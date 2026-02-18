"""Real topic clustering service using sentence-transformers and HDBSCAN"""
import logging
import json
from typing import List, Dict, Optional
from datetime import datetime
from ..models.article import Article, Cluster
from ..core.exceptions import ClusteringError
from ..core.error_handler import handle_errors

logger = logging.getLogger(__name__)

# Optional imports
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    logger.warning("numpy not available - advanced clustering disabled")

# Lazy loading of ML models
_embedding_model = None


def _load_embedding_model(model_name: str = "all-MiniLM-L6-v2"):
    """Lazy-load the sentence transformer model"""
    global _embedding_model

    if _embedding_model is not None:
        return _embedding_model

    try:
        from sentence_transformers import SentenceTransformer

        logger.info(f"Loading embedding model: {model_name}")
        _embedding_model = SentenceTransformer(model_name)
        logger.info(f"Embedding model {model_name} loaded successfully")
        return _embedding_model

    except Exception as e:
        logger.error(f"Failed to load embedding model: {e}")
        raise ClusteringError(f"Embedding model loading failed: {e}")


class TopicClusterer:
    """
    Production topic clustering service using sentence-transformers and HDBSCAN.
    Falls back to keyword-based clustering if ML models aren't available.
    """

    KEYWORD_LABELS = {
        0: "Technology & AI",
        1: "Climate & Environment",
        2: "Politics & Policy",
        3: "Health & Science",
        4: "Business & Economy",
        5: "Sports & Entertainment",
        6: "World News",
        7: "Miscellaneous",
    }

    def __init__(self, embedding_model_name: str = "all-MiniLM-L6-v2",
                 min_cluster_size: int = 5, min_samples: int = 3,
                 max_cluster_articles: int = 50, similarity_threshold: float = 0.7):
        self.embedding_model_name = embedding_model_name
        self.min_cluster_size = min_cluster_size
        self.min_samples = min_samples
        self.max_cluster_articles = max_cluster_articles
        self.similarity_threshold = similarity_threshold
        self.clusters: Dict[int, Cluster] = {}
        self._model_loaded = False
        logger.info("TopicClusterer initialized")

    def _ensure_model(self):
        """Ensure embedding model is loaded"""
        if not self._model_loaded:
            try:
                _load_embedding_model(self.embedding_model_name)
                self._model_loaded = True
            except Exception as e:
                logger.warning(f"Embedding model not available, using keyword fallback: {e}")

    @handle_errors
    def generate_embeddings(self, texts: List[str]) -> Optional[np.ndarray]:
        """
        Generate semantic embeddings for texts.

        Args:
            texts: List of text strings

        Returns:
            numpy array of embeddings or None if model unavailable
        """
        self._ensure_model()

        if not self._model_loaded or _embedding_model is None:
            return None

        try:
            embeddings = _embedding_model.encode(
                texts, show_progress_bar=False, convert_to_numpy=True
            )
            logger.debug(f"Generated {len(embeddings)} embeddings of dim {embeddings.shape[1]}")
            return embeddings
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            return None

    @handle_errors
    def cluster_articles(self, articles: List[Article]) -> Dict[int, List[str]]:
        """
        Cluster articles by topic using HDBSCAN or keyword fallback.

        Args:
            articles: List of articles to cluster

        Returns:
            Dictionary mapping cluster_id to list of article_ids
        """
        if not articles:
            return {}

        logger.info(f"Clustering {len(articles)} articles")

        # Prepare texts for embedding (title + first 200 words of content)
        texts = []
        for article in articles:
            text = article.title
            if hasattr(article, 'compressed_content') and article.compressed_content:
                try:
                    from ..services.compressor import ContentCompressor
                    comp = ContentCompressor()
                    content = comp.decompress(article.compressed_content)
                    words = content.split()[:200]
                    text += " " + " ".join(words)
                except Exception:
                    pass
            texts.append(text)

        # Try HDBSCAN clustering with embeddings
        embeddings = self.generate_embeddings(texts)

        if embeddings is not None and len(articles) >= self.min_cluster_size:
            return self._hdbscan_cluster(articles, embeddings)
        else:
            return self._keyword_cluster(articles)

    def _hdbscan_cluster(self, articles: List[Article], embeddings: np.ndarray) -> Dict[int, List[str]]:
        """Cluster using HDBSCAN algorithm"""
        try:
            import hdbscan

            # Adjust min_cluster_size if we have too few articles
            effective_min_cluster = min(self.min_cluster_size, max(2, len(articles) // 3))
            effective_min_samples = min(self.min_samples, effective_min_cluster)

            clusterer = hdbscan.HDBSCAN(
                min_cluster_size=effective_min_cluster,
                min_samples=effective_min_samples,
                metric='euclidean',
                cluster_selection_method='eom',
            )

            labels = clusterer.fit_predict(embeddings)

            # Build cluster mapping
            clusters: Dict[int, List[str]] = {}
            now = datetime.now()

            for i, (article, label) in enumerate(zip(articles, labels)):
                # HDBSCAN uses -1 for noise; assign to a "Miscellaneous" cluster
                cluster_id = int(label) if label >= 0 else 999

                if cluster_id not in clusters:
                    clusters[cluster_id] = []
                clusters[cluster_id].append(article.id)
                article.cluster_id = cluster_id

            # Generate cluster labels using TF-IDF
            for cluster_id, article_ids in clusters.items():
                cluster_articles = [a for a in articles if a.id in article_ids]
                label = self._generate_tfidf_label(cluster_articles, embeddings, articles)

                # Get centroid
                cluster_indices = [i for i, a in enumerate(articles) if a.id in article_ids]
                centroid = np.mean(embeddings[cluster_indices], axis=0) if cluster_indices else None

                self.clusters[cluster_id] = Cluster(
                    id=cluster_id,
                    label=label,
                    article_ids=article_ids,
                    centroid=centroid,
                    created_at=now,
                    updated_at=now,
                )

            # Handle sub-clustering for large clusters
            for cluster_id, article_ids in list(clusters.items()):
                if len(article_ids) > self.max_cluster_articles:
                    self._sub_cluster(cluster_id, articles, embeddings)

            logger.info(f"HDBSCAN created {len(clusters)} clusters")
            return clusters

        except ImportError:
            logger.warning("HDBSCAN not available, falling back to keyword clustering")
            return self._keyword_cluster(articles)
        except Exception as e:
            logger.error(f"HDBSCAN clustering failed: {e}")
            return self._keyword_cluster(articles)

    def _generate_tfidf_label(self, cluster_articles: List[Article],
                               all_embeddings: np.ndarray, all_articles: List[Article]) -> str:
        """Generate cluster label using TF-IDF of article titles"""
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer

            titles = [a.title for a in cluster_articles]
            if not titles:
                return "Miscellaneous"

            vectorizer = TfidfVectorizer(max_features=100, stop_words='english', max_df=0.9)
            tfidf_matrix = vectorizer.fit_transform(titles)
            feature_names = vectorizer.get_feature_names_out()

            # Get top 3 keywords
            mean_tfidf = tfidf_matrix.mean(axis=0).A1
            top_indices = mean_tfidf.argsort()[-3:][::-1]
            keywords = [feature_names[i] for i in top_indices if mean_tfidf[i] > 0]

            if keywords:
                return " & ".join(word.title() for word in keywords)
            return "Miscellaneous"

        except Exception as e:
            logger.debug(f"TF-IDF label generation failed: {e}")
            return "Miscellaneous"

    def _sub_cluster(self, cluster_id: int, articles: List[Article], embeddings: np.ndarray):
        """Split large clusters into sub-clusters"""
        cluster = self.clusters.get(cluster_id)
        if not cluster or len(cluster.article_ids) <= self.max_cluster_articles:
            return

        logger.info(f"Sub-clustering cluster {cluster_id} with {len(cluster.article_ids)} articles")

        # Get articles and embeddings for this cluster
        cluster_articles = [a for a in articles if a.id in cluster.article_ids]
        cluster_indices = [i for i, a in enumerate(articles) if a.id in cluster.article_ids]
        cluster_embeddings = embeddings[cluster_indices]

        try:
            import hdbscan

            sub_clusterer = hdbscan.HDBSCAN(
                min_cluster_size=max(2, len(cluster_articles) // 5),
                metric='euclidean',
            )
            sub_labels = sub_clusterer.fit_predict(cluster_embeddings)

            # Create sub-clusters with IDs like cluster_id * 100 + sub_id
            now = datetime.now()
            for sub_id in set(sub_labels):
                if sub_id == -1:
                    continue
                new_id = cluster_id * 100 + sub_id + 1
                sub_article_ids = [
                    cluster_articles[i].id
                    for i, l in enumerate(sub_labels) if l == sub_id
                ]
                if sub_article_ids:
                    self.clusters[new_id] = Cluster(
                        id=new_id,
                        label=f"{cluster.label} (Sub-{sub_id + 1})",
                        article_ids=sub_article_ids,
                        centroid=None,
                        created_at=now,
                        updated_at=now,
                    )

        except Exception as e:
            logger.warning(f"Sub-clustering failed: {e}")

    def _keyword_cluster(self, articles: List[Article]) -> Dict[int, List[str]]:
        """Fallback keyword-based clustering"""
        keyword_map = {
            0: ['ai', 'artificial', 'technology', 'tech', 'software', 'digital', 'computer', 'robot', 'machine'],
            1: ['climate', 'environment', 'green', 'energy', 'carbon', 'warming', 'pollution', 'weather'],
            2: ['politics', 'policy', 'government', 'election', 'president', 'congress', 'vote', 'party'],
            3: ['health', 'science', 'research', 'medical', 'disease', 'vaccine', 'hospital', 'study'],
            4: ['business', 'economy', 'market', 'finance', 'stock', 'trade', 'company', 'revenue'],
            5: ['sports', 'entertainment', 'game', 'movie', 'music', 'team', 'player', 'win'],
            6: ['world', 'international', 'war', 'peace', 'crisis', 'nation', 'country', 'global'],
        }

        clusters: Dict[int, List[str]] = {}
        now = datetime.now()

        for article in articles:
            title_lower = article.title.lower()
            assigned = False

            for cluster_id, keywords in keyword_map.items():
                if any(word in title_lower for word in keywords):
                    if cluster_id not in clusters:
                        clusters[cluster_id] = []
                    clusters[cluster_id].append(article.id)
                    article.cluster_id = cluster_id
                    assigned = True
                    break

            if not assigned:
                misc_id = 7
                if misc_id not in clusters:
                    clusters[misc_id] = []
                clusters[misc_id].append(article.id)
                article.cluster_id = misc_id

        for cluster_id, article_ids in clusters.items():
            label = self.KEYWORD_LABELS.get(cluster_id, f"Topic {cluster_id}")
            self.clusters[cluster_id] = Cluster(
                id=cluster_id,
                label=label,
                article_ids=article_ids,
                centroid=None,
                created_at=now,
                updated_at=now,
            )

        logger.info(f"Keyword clustering created {len(clusters)} clusters")
        return clusters

    @handle_errors
    def get_cluster(self, cluster_id: int) -> Optional[Cluster]:
        """Get cluster by ID"""
        return self.clusters.get(cluster_id)

    @handle_errors
    def get_all_clusters(self) -> List[Cluster]:
        """Get all clusters"""
        return list(self.clusters.values())

    @handle_errors
    def generate_cluster_label(self, cluster_id: int) -> str:
        """Generate descriptive label for cluster"""
        cluster = self.clusters.get(cluster_id)
        if cluster:
            return cluster.label
        return f"Topic {cluster_id}"
