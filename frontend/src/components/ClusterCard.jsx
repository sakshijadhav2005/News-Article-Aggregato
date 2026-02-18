import React from 'react';
import { Link } from 'react-router-dom';

function ClusterCard({ cluster }) {
    return (
        <Link
            to={`/clusters/${cluster.id}`}
            className="glass-card cluster-card"
            id={`cluster-card-${cluster.id}`}
            style={{ textDecoration: 'none' }}
        >
            <div className="cluster-label">{cluster.label}</div>
            <div className="cluster-count">{cluster.article_count || 0}</div>
            <div className="cluster-subtitle">articles in this topic</div>
        </Link>
    );
}

export default ClusterCard;
