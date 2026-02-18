import React from 'react';

function StatsCards({ stats }) {
    if (!stats) return null;

    const cards = [
        { label: 'Total Articles', value: stats.total_articles || 0, icon: '📰' },
        { label: 'Topic Clusters', value: stats.total_clusters || 0, icon: '🏷️' },
        { label: 'Cache Size', value: stats.cache_size || 0, icon: '⚡' },
        { label: 'Sources', value: stats.sources?.length || 0, icon: '🌐' },
    ];

    return (
        <div className="stats-grid" id="stats-grid">
            {cards.map((card) => (
                <div className="glass-card stat-card" key={card.label}>
                    <div style={{ fontSize: '1.5rem', marginBottom: '8px' }}>{card.icon}</div>
                    <div className="stat-value">{card.value}</div>
                    <div className="stat-label">{card.label}</div>
                </div>
            ))}
        </div>
    );
}

export default StatsCards;
