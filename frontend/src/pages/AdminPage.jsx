import React, { useState, useEffect } from 'react';
import api from '../services/api';
import StatsCards from '../components/StatsCards';

function AdminPage() {
    const [stats, setStats] = useState(null);
    const [fetchCount, setFetchCount] = useState(20);
    const [isFetching, setIsFetching] = useState(false);
    const [logs, setLogs] = useState([]);
    const [healthStatus, setHealthStatus] = useState(null);

    // Load stats on mount
    useEffect(() => {
        loadStats();
        checkHealth();
    }, []);

    const loadStats = async () => {
        try {
            const res = await api.getStats();
            setStats(res.data);
        } catch (err) {
            addLog('error', `Failed to load stats: ${err.message}`);
        }
    };

    const checkHealth = async () => {
        try {
            const res = await api.healthCheck();
            setHealthStatus(res.data);
            addLog('info', 'Health check passed');
        } catch (err) {
            addLog('error', `Health check failed: ${err.message}`);
        }
    };

    const handleFetch = async () => {
        setIsFetching(true);
        addLog('info', `Starting article fetch (count: ${fetchCount})...`);

        try {
            const res = await api.triggerFetch(fetchCount);
            const data = res.data;

            addLog('success', `Fetch complete! Fetched: ${data.fetched}, Stored: ${data.stored}, Summarized: ${data.summarized}, Clustered: ${data.clustered}`);

            if (data.errors && data.errors.length > 0) {
                data.errors.forEach((err) => addLog('warning', `Error: ${err}`));
            }

            // Reload stats
            await loadStats();
        } catch (err) {
            addLog('error', `Fetch failed: ${err.message}`);
        } finally {
            setIsFetching(false);
        }
    };

    const addLog = (type, message) => {
        const timestamp = new Date().toLocaleTimeString();
        setLogs((prev) => [{ type, message, timestamp }, ...prev].slice(0, 50));
    };

    const getLogColor = (type) => {
        switch (type) {
            case 'error': return 'var(--error)';
            case 'warning': return 'var(--warning)';
            case 'success': return 'var(--success)';
            default: return 'var(--text-secondary)';
        }
    };

    return (
        <div className="admin-panel" id="admin-page">
            <div className="page-header">
                <h1 className="page-title">Admin Panel</h1>
                <p className="page-subtitle">Manage article fetching, system health, and statistics</p>
            </div>

            {/* Stats */}
            <StatsCards stats={stats} />

            {/* Health Status */}
            {healthStatus && (
                <div className="glass-card" style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <span className={`badge badge-${healthStatus.status === 'healthy' ? 'success' : 'error'}`}>
                        {healthStatus.status === 'healthy' ? '● Healthy' : '● Unhealthy'}
                    </span>
                    <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                        Last checked: {new Date().toLocaleTimeString()}
                    </span>
                </div>
            )}

            {/* Admin Actions */}
            <div className="admin-actions">
                {/* Fetch Articles */}
                <div className="glass-card admin-action-card" id="fetch-action">
                    <h3 className="admin-action-title">📰 Fetch Articles</h3>
                    <p className="admin-action-desc">
                        Trigger a manual fetch from RSS feeds and NewsAPI. Articles will be automatically
                        compressed, summarized, and clustered.
                    </p>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Count:</label>
                        <input
                            type="number"
                            className="fetch-count-input"
                            value={fetchCount}
                            onChange={(e) => setFetchCount(Math.max(1, Math.min(100, parseInt(e.target.value) || 1)))}
                            min="1"
                            max="100"
                            id="fetch-count-input"
                        />
                        <button
                            className="btn btn-primary"
                            onClick={handleFetch}
                            disabled={isFetching}
                            id="fetch-button"
                        >
                            {isFetching ? (
                                <>
                                    <span className="loading-spinner" style={{ width: '16px', height: '16px', borderWidth: '2px' }}></span>
                                    Fetching...
                                </>
                            ) : (
                                '🚀 Start Fetch'
                            )}
                        </button>
                    </div>
                </div>

                {/* System Health */}
                <div className="glass-card admin-action-card" id="health-action">
                    <h3 className="admin-action-title">🏥 System Health</h3>
                    <p className="admin-action-desc">
                        Check the health of all system components including database, cache, and ML models.
                    </p>
                    <button
                        className="btn btn-secondary"
                        onClick={checkHealth}
                        id="health-check-button"
                    >
                        🔍 Check Health
                    </button>
                </div>
            </div>

            {/* Activity Log */}
            <div className="glass-card admin-log" id="activity-log">
                <h3 style={{ marginBottom: '1rem', fontSize: '1rem', fontWeight: '600' }}>
                    📋 Activity Log
                </h3>
                {logs.length > 0 ? (
                    logs.map((log, i) => (
                        <div className="admin-log-entry" key={i}>
                            <span className="admin-log-time">[{log.timestamp}]</span>
                            <span className="admin-log-message" style={{ color: getLogColor(log.type) }}>
                                {log.message}
                            </span>
                        </div>
                    ))
                ) : (
                    <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', textAlign: 'center', padding: '2rem' }}>
                        No activity yet. Trigger a fetch to see activity logs.
                    </div>
                )}
            </div>
        </div>
    );
}

export default AdminPage;
