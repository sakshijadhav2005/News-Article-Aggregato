import React from 'react';

function Footer() {
    return (
        <footer className="footer" id="app-footer">
            <div className="footer-inner">
                <div className="footer-text">
                    © {new Date().getFullYear()} NewsAgg — AI-Powered News Aggregator
                </div>
                <div className="footer-links">
                    <a href="https://github.com" target="_blank" rel="noopener noreferrer">GitHub</a>
                    <a href="/docs" target="_blank" rel="noopener noreferrer">API Docs</a>
                </div>
            </div>
        </footer>
    );
}

export default Footer;
