/**
 * Custom hook for article operations
 */
import { useState, useEffect, useCallback } from 'react';
import api from '../services/api';

export function useArticles(initialParams = {}) {
    const [articles, setArticles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [total, setTotal] = useState(0);
    const [page, setPage] = useState(initialParams.page || 1);
    const [filters, setFilters] = useState({
        source: initialParams.source || '',
        search: initialParams.search || '',
        cluster_id: initialParams.cluster_id || null,
        date_from: initialParams.date_from || '',
        date_to: initialParams.date_to || '',
    });

    const fetchArticles = useCallback(async () => {
        setLoading(true);
        setError(null);

        try {
            const params = { page, page_size: 20 };
            if (filters.source) params.source = filters.source;
            if (filters.search) params.search = filters.search;
            if (filters.cluster_id) params.cluster_id = filters.cluster_id;
            if (filters.date_from) params.date_from = filters.date_from;
            if (filters.date_to) params.date_to = filters.date_to;

            const response = await api.getArticles(params);
            setArticles(response.data || []);
            setTotal(response.total || 0);
        } catch (err) {
            setError(err.message);
            setArticles([]);
        } finally {
            setLoading(false);
        }
    }, [page, filters]);

    useEffect(() => {
        fetchArticles();
    }, [fetchArticles]);

    const updateFilters = (newFilters) => {
        setFilters(prev => ({ ...prev, ...newFilters }));
        setPage(1);
    };

    const totalPages = Math.ceil(total / 20);

    return {
        articles,
        loading,
        error,
        total,
        page,
        totalPages,
        filters,
        setPage,
        updateFilters,
        refetch: fetchArticles,
    };
}

export function useArticle(articleId) {
    const [article, setArticle] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!articleId) return;

        const fetch = async () => {
            setLoading(true);
            setError(null);
            try {
                const response = await api.getArticle(articleId);
                setArticle(response.data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetch();
    }, [articleId]);

    return { article, loading, error };
}

export default useArticles;
