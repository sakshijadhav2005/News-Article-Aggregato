import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useClusters, useClusterArticles } from '../hooks/useClusters';
import ClusterCard from '../components/ClusterCard';
import ArticleCard from '../components/ArticleCard';
import Pagination from '../components/Pagination';

function ClustersPage() {
  const navigate = useNavigate();
  const { clusterId } = useParams();
  const { clusters, loading, error, refetch } = useClusters();
  const [clusterPage, setClusterPage] = useState(1);

  // If a cluster ID is in the URL, show that cluster's articles
  const selectedCluster = clusterId ? parseInt(clusterId) : null;
  const {
    articles: clusterArticles,
    total: clusterTotal,
    loading: clusterLoading,
    error: clusterError,
  } = useClusterArticles(selectedCluster, clusterPage);

  const clusterInfo = clusters.find(c => c.id === selectedCluster);

  const handleArticleClick = (article) => {
    navigate(`/articles/${article.id}`);
  };

  // Cluster detail view
  if (selectedCluster !== null) {
    return (
      <div id="cluster-detail-page">
        <button
          className="btn btn-secondary btn-sm back-btn"
          onClick={() => navigate('/clusters')}
        >
          ← Back to Clusters
        </button>

        <div className="page-header">
          <h1 className="page-title">
            {clusterInfo?.label || `Cluster #${selectedCluster}`}
          </h1>
          <p className="page-subtitle">
            {clusterTotal} articles in this topic cluster
          </p>
        </div>

        {clusterLoading && (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <div className="loading-text">Loading cluster articles...</div>
          </div>
        )}

        {clusterError && (
          <div className="error-container">
            <div className="error-icon">⚠️</div>
            <div className="error-message">{clusterError}</div>
          </div>
        )}

        {!clusterLoading && !clusterError && (
          <>
            {clusterArticles.length > 0 ? (
              <div className="articles-grid">
                {clusterArticles.map((article) => (
                  <ArticleCard
                    key={article.id}
                    article={article}
                    onClick={handleArticleClick}
                  />
                ))}
              </div>
            ) : (
              <div className="empty-container">
                <div className="empty-icon">📭</div>
                <p className="empty-message">No articles in this cluster</p>
              </div>
            )}

            <Pagination
              page={clusterPage}
              totalPages={Math.ceil(clusterTotal / 20)}
              onPageChange={setClusterPage}
            />
          </>
        )}
      </div>
    );
  }

  // Clusters list view
  return (
    <div id="clusters-page">
      <div className="page-header">
        <h1 className="page-title">Topic Clusters</h1>
        <p className="page-subtitle">
          Articles organized by AI-detected topics
        </p>
      </div>

      {loading && (
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <div className="loading-text">Loading clusters...</div>
        </div>
      )}

      {error && (
        <div className="error-container">
          <div className="error-icon">⚠️</div>
          <div className="error-message">{error}</div>
          <button className="btn btn-primary btn-sm" onClick={refetch}>Try Again</button>
        </div>
      )}

      {!loading && !error && (
        <>
          {clusters.length > 0 ? (
            <div className="clusters-grid">
              {clusters.map((cluster) => (
                <ClusterCard key={cluster.id} cluster={cluster} />
              ))}
            </div>
          ) : (
            <div className="empty-container">
              <div className="empty-icon">🏷️</div>
              <p className="empty-message">
                No clusters yet. Articles need to be fetched and clustered first.
              </p>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default ClustersPage;
