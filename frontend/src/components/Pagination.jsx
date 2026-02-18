import React from 'react';

function Pagination({ page, totalPages, onPageChange }) {
    if (totalPages <= 1) return null;

    const getPageNumbers = () => {
        const pages = [];
        const maxVisible = 5;

        let start = Math.max(1, page - Math.floor(maxVisible / 2));
        let end = Math.min(totalPages, start + maxVisible - 1);

        if (end - start < maxVisible - 1) {
            start = Math.max(1, end - maxVisible + 1);
        }

        for (let i = start; i <= end; i++) {
            pages.push(i);
        }

        return pages;
    };

    return (
        <div className="pagination" id="pagination-controls">
            <button
                className="pagination-btn"
                onClick={() => onPageChange(page - 1)}
                disabled={page <= 1}
                aria-label="Previous page"
            >
                ‹
            </button>

            {getPageNumbers().map((num) => (
                <button
                    key={num}
                    className={`pagination-btn ${num === page ? 'active' : ''}`}
                    onClick={() => onPageChange(num)}
                    aria-label={`Page ${num}`}
                >
                    {num}
                </button>
            ))}

            <span className="pagination-info">
                of {totalPages}
            </span>

            <button
                className="pagination-btn"
                onClick={() => onPageChange(page + 1)}
                disabled={page >= totalPages}
                aria-label="Next page"
            >
                ›
            </button>
        </div>
    );
}

export default Pagination;
