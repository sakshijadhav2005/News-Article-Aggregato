/**
 * Custom hook for cluster operations
 */
import { useState, useEffect, useCallback } from 'react';
import api from '../services/api';

export function useClusters() {
    const [clusters, setClusters] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchClusters = useCallback(async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await api.getClusters();
            setClusters(response.data || []);
        } catch (err) {
            setError(err.message);
            setClusters([]);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchClusters();
    }, [fetchClusters]);

    return { clusters, loading, error, refetch: fetchClusters };
}

export function useClusterArticles(clusterId, page = 1) {
    const [articles, setArticles] = useState([]);
    const [total, setTotal] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (clusterId === null || clusterId === undefined) return;

        const fetch = async () => {
            setLoading(true);
            setError(null);
            try {
                const response = await api.getClusterArticles(clusterId, { page, page_size: 20 });
                setArticles(response.data || []);
                setTotal(response.total || 0);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetch();
    }, [clusterId, page]);

    return { articles, total, loading, error };
}

export default useClusters;
