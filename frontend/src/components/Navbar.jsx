import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import useTheme from '../hooks/useTheme';

function Navbar() {
    const location = useLocation();
    const { darkMode, toggleTheme } = useTheme();

    const isActive = (path) => location.pathname === path ? 'active' : '';

    return (
        <nav className="navbar" id="main-navbar">
            <div className="navbar-inner">
                <Link to="/" className="navbar-brand">
                    <div className="navbar-logo">N</div>
                    <span className="navbar-title">NewsAgg</span>
                </Link>

                <ul className="navbar-links">
                    <li><Link to="/" className={isActive('/')}>Home</Link></li>
                    <li><Link to="/articles" className={isActive('/articles')}>Articles</Link></li>
                    <li><Link to="/clusters" className={isActive('/clusters')}>Clusters</Link></li>
                    <li><Link to="/admin" className={isActive('/admin')}>Admin</Link></li>
                </ul>

                <div className="navbar-actions">
                    <button
                        className="theme-toggle"
                        onClick={toggleTheme}
                        aria-label="Toggle theme"
                        id="theme-toggle-btn"
                    >
                        {darkMode ? '☀️' : '🌙'}
                    </button>
                </div>
            </div>
        </nav>
    );
}

export default Navbar;
