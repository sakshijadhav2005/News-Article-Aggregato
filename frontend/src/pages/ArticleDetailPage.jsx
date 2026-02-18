import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useArticle } from '../hooks/useArticles';
import { formatFullDate } from '../utils/formatters';

function ArticleDetailPage() {
    const { id } = useParams();
    const navigate = useNavigate();
    const { article, loading, error } = useArticle(id);

    if (loading) {
        return (
            <div className="loading-container">
                <div className="loading-spinner"></div>
                <div className="loading-text">Loading article...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="error-container">
                <div className="error-icon">⚠️</div>
                <div className="error-message">{error}</div>
                <button className="btn btn-primary btn-sm" onClick={() => navigate(-1)}>Go Back</button>
            </div>
        );
    }

    if (!article) {
        return (
            <div className="empty-container">
                <div className="empty-icon">🔍</div>
                <div className="empty-message">Article not found</div>
                <button className="btn btn-primary btn-sm" onClick={() => navigate('/articles')}>
                    Browse Articles
                </button>
            </div>
        );
    }

    return (
        <div className="article-detail" id="article-detail-page">
            <button
                className="btn btn-secondary btn-sm back-btn"
                onClick={() => navigate(-1)}
                id="back-button"
            >
                ← Back
            </button>

            <div className="article-detail-header">
                <h1 className="article-detail-title">{article.title}</h1>

                <div className="article-detail-meta">
                    <span className="article-source">{article.source}</span>
                    {article.author && <span>By {article.author}</span>}
                    <span>{formatFullDate(article.published_date)}</span>
                    {article.cluster_id !== null && article.cluster_id !== undefined && (
                        <span className="badge badge-info">Cluster #{article.cluster_id}</span>
                    )}
                </div>
            </div>

            {/* Summary */}
            {article.summary && (
                <div className="article-detail-summary">
                    <strong>AI Summary:</strong> {article.summary}
                </div>
            )}

            {/* Full Content */}
            <div className="article-detail-content">
                {article.content ? (
                    article.content.split('\n').map((paragraph, idx) => (
                        paragraph.trim() ? <p key={idx}>{paragraph}</p> : null
                    ))
                ) : (
                    <p style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>
                        Full content not available.{' '}
                        {article.url && (
                            <a href={article.url} target="_blank" rel="noopener noreferrer">
                                Read on original site →
                            </a>
                        )}
                    </p>
                )}
            </div>

            {/* Original Source Link */}
            {article.url && (
                <div style={{ marginTop: '2rem', paddingTop: '1.5rem', borderTop: '1px solid var(--border-glass)' }}>
                    <a
                        href={article.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn btn-secondary"
                    >
                        🔗 Read Original Article
                    </a>
                </div>
            )}
        </div>
    );
}

export default ArticleDetailPage;
