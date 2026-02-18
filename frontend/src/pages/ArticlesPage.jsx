import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useArticles } from '../hooks/useArticles';
import api from '../services/api';
import ArticleCard from '../components/ArticleCard';
import SearchFilters from '../components/SearchFilters';
import Pagination from '../components/Pagination';

function ArticlesPage() {
  const navigate = useNavigate();
  const {
    articles, loading, error, total,
    page, totalPages, filters,
    setPage, updateFilters, refetch,
  } = useArticles();

  const [sources, setSources] = useState([]);

  // Fetch available sources from stats
  useEffect(() => {
    const fetchSources = async () => {
      try {
        const res = await api.getStats();
        setSources(res.data?.sources || []);
      } catch (e) {
        console.warn('Failed to fetch sources:', e);
      }
    };
    fetchSources();
  }, []);

  const handleArticleClick = (article) => {
    navigate(`/articles/${article.id}`);
  };

  return (
    <div id="articles-page">
      <div className="page-header">
        <h1 className="page-title">Articles</h1>
        <p className="page-subtitle">
          {total > 0 ? `${total} articles found` : 'Explore news from multiple sources'}
        </p>
      </div>

      {/* Search & Filters */}
      <SearchFilters
        filters={filters}
        onFilterChange={updateFilters}
        sources={sources}
      />

      {/* Loading State */}
      {loading && (
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <div className="loading-text">Loading articles...</div>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="error-container">
          <div className="error-icon">⚠️</div>
          <div className="error-message">{error}</div>
          <button className="btn btn-primary btn-sm" onClick={refetch}>Try Again</button>
        </div>
      )}

      {/* Articles Grid */}
      {!loading && !error && (
        <>
          {articles.length > 0 ? (
            <div className="articles-grid">
              {articles.map((article) => (
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
              <p className="empty-message">No articles match your filters.</p>
              <button className="btn btn-secondary btn-sm" onClick={() => updateFilters({
                search: '', source: '', date_from: '', date_to: '', cluster_id: null
              })}>
                Clear Filters
              </button>
            </div>
          )}

          {/* Pagination */}
          <Pagination
            page={page}
            totalPages={totalPages}
            onPageChange={setPage}
          />
        </>
      )}
    </div>
  );
}

export default ArticlesPage;
