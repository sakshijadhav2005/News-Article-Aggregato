import React from 'react';

function SearchFilters({ filters, onFilterChange, sources = [] }) {

    const handleSearchChange = (e) => {
        onFilterChange({ search: e.target.value });
    };

    const handleSourceChange = (e) => {
        onFilterChange({ source: e.target.value });
    };

    const handleDateFromChange = (e) => {
        onFilterChange({ date_from: e.target.value || '' });
    };

    const handleDateToChange = (e) => {
        onFilterChange({ date_to: e.target.value || '' });
    };

    return (
        <div className="search-filters" id="search-filters">
            <div className="search-wrapper">
                <span className="search-icon">🔍</span>
                <input
                    type="text"
                    className="search-input"
                    placeholder="Search articles..."
                    value={filters.search || ''}
                    onChange={handleSearchChange}
                    id="search-input"
                />
            </div>

            <select
                className="filter-select"
                value={filters.source || ''}
                onChange={handleSourceChange}
                id="source-filter"
            >
                <option value="">All Sources</option>
                {sources.map((src) => (
                    <option key={src} value={src}>{src}</option>
                ))}
            </select>

            <input
                type="date"
                className="date-input"
                value={filters.date_from || ''}
                onChange={handleDateFromChange}
                placeholder="From date"
                id="date-from-filter"
            />

            <input
                type="date"
                className="date-input"
                value={filters.date_to || ''}
                onChange={handleDateToChange}
                placeholder="To date"
                id="date-to-filter"
            />
        </div>
    );
}

export default SearchFilters;
