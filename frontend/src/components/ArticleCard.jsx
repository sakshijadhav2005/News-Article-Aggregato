import React from 'react';

function ArticleCard({ article, onClick }) {
    const { title, summary, source, author, published_date } = article;

    const formatDate = (dateStr) => {
        if (!dateStr) return '';
        const d = new Date(dateStr);
        const now = new Date();
        const diff = now - d;
        const hours = Math.floor(diff / (1000 * 60 * 60));
        if (hours < 1) return 'Just now';
        if (hours < 24) return `${hours}h ago`;
        const days = Math.floor(hours / 24);
        if (days < 7) return `${days}d ago`;
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    };

    return (
        <div
            className="glass-card article-card"
            onClick={() => onClick && onClick(article)}
            role="article"
            tabIndex={0}
            id={`article-card-${article.id}`}
        >
            <div className="article-card-header">
                <span className="article-source">{source}</span>
                <span className="article-date">{formatDate(published_date)}</span>
            </div>

            <h3 className="article-title">{title}</h3>

            {summary && (
                <p className="article-summary">{summary}</p>
            )}

            <div className="article-footer">
                <span className="article-author">
                    {author ? `By ${author}` : ''}
                </span>
                <span className="article-read-more">Read more</span>
            </div>
        </div>
    );
}

export default ArticleCard;
