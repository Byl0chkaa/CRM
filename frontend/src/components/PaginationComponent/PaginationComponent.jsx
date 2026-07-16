import React from 'react';
import './PaginationComponent.css';

const PAGE_WINDOW = 7;

function getPageItems(currentPage, totalPages) {
    if (totalPages <= PAGE_WINDOW + 2) {
        return Array.from({length: totalPages}, (_, i) => i + 1);
    }

    const half = Math.floor(PAGE_WINDOW / 2);

    let start = currentPage - half;
    let end = currentPage + half;

    if (start < 1) {
        start = 1;
        end = start + PAGE_WINDOW - 1;
    }
    if (end > totalPages) {
        end = totalPages;
        start = end - PAGE_WINDOW + 1;
        if (start < 1) start = 1;
    }

    const window = [];
    for (let i = start; i <= end; i++) window.push(i);

    const items = [];

    if (start > 1) {
        items.push(1);
        if (start > 2) items.push('ellipsis');
    }

    items.push(...window);

    if (end < totalPages) {
        if (end < totalPages - 1) items.push('ellipsis');
        items.push(totalPages);
    }

    return items;
}

const PaginationComponent = ({currentPage, totalPages, onPageChange}) => {
    if (totalPages <= 1) return null;

    const items = getPageItems(currentPage, totalPages);

    return (
        <div className="pagination">
            {currentPage > 1 && (
                <button
                    className="pagination_btn pagination_arrow"
                    onClick={() => onPageChange(currentPage - 1)}
                >
                    {'<'}
                </button>
            )}

            {items.map((item, idx) =>
                item === 'ellipsis' ? (
                    <span key={`ellipsis-${idx}`} className="pagination_ellipsis">
                        ...
                    </span>
                ) : (
                    <button
                        key={item}
                        className={
                            'pagination_btn' +
                            (item === currentPage ? ' pagination_btn-active' : '')
                        }
                        onClick={() => onPageChange(item)}
                    >
                        {item}
                    </button>
                )
            )}

            {currentPage < totalPages && (
                <button
                    className="pagination_btn pagination_arrow"
                    onClick={() => onPageChange(currentPage + 1)}
                >
                    {'>'}
                </button>
            )}
        </div>
    );
};

export default PaginationComponent;