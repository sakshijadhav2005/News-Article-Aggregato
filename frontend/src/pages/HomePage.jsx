import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';
import ArticleCard from '../components/ArticleCard';
import ClusterCard from '../components/ClusterCard';
import StatsCards from '../components/StatsCards';

function HomePage() {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [latestArticles, setLatestArticles] = useState([]);
  const [clusters, setClusters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [statsRes, articlesRes, clustersRes] = await Promise.allSettled([
          api.getStats(),
          api.getArticles({ page_size: 6 }),
          api.getClusters(),
        ]);

        if (statsRes.status === 'fulfilled') setStats(statsRes.value.data);
        if (articlesRes.status === 'fulfilled') setLatestArticles(articlesRes.value.data || []);
        if (clustersRes.status === 'fulfilled') setClusters(clustersRes.value.data || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleArticleClick = (article) => {
    navigate(`/articles/${article.id}`);
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <div className="loading-text">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <div id="home-page">
      {/* Hero Section */}
      <section className="hero">
        <h1 className="hero-title">AI-Powered News Intelligence</h1>
        <p className="hero-subtitle">
          Aggregate, summarize, and cluster news articles using cutting-edge AI.
          Stay informed with intelligent insights from multiple sources.
        </p>
        <div className="hero-actions">
          <Link to="/articles" className="btn btn-primary">
            📰 Browse Articles
          </Link>
          <Link to="/clusters" className="btn btn-secondary">
            🏷️ View Clusters
          </Link>
        </div>
      </section>

      {/* Stats */}
      <StatsCards stats={stats} />

      {/* Latest Articles */}
      <section style={{ marginBottom: '3rem' }}>
        <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h2 className="page-title">Latest Articles</h2>
            <p className="page-subtitle">Most recent news from all sources</p>
          </div>
          <Link to="/articles" className="btn btn-secondary btn-sm">
            View All →
          </Link>
        </div>

        {latestArticles.length > 0 ? (
          <div className="articles-grid">
            {latestArticles.map((article) => (
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
            <p className="empty-message">
              No articles yet. Visit the <Link to="/admin">Admin Panel</Link> to fetch articles.
            </p>
          </div>
        )}
      </section>

      {/* Topic Clusters */}
      {clusters.length > 0 && (
        <section>
          <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <h2 className="page-title">Topic Clusters</h2>
              <p className="page-subtitle">Articles grouped by AI-detected topics</p>
            </div>
            <Link to="/clusters" className="btn btn-secondary btn-sm">
              View All →
            </Link>
          </div>

          <div className="clusters-grid">
            {clusters.slice(0, 6).map((cluster) => (
              <ClusterCard
                key={cluster.id}
                cluster={cluster}
              />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

export default HomePage;
