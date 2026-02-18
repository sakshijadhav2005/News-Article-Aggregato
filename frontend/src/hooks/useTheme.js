/**
 * Custom hook for dark mode / theme management
 */
import { useState, useEffect } from 'react';

export function useTheme() {
    const [darkMode, setDarkMode] = useState(() => {
        const saved = localStorage.getItem('theme');
        if (saved) return saved === 'dark';
        return window.matchMedia('(prefers-color-scheme: dark)').matches;
    });

    useEffect(() => {
        const root = document.documentElement;
        if (darkMode) {
            root.classList.add('dark');
            localStorage.setItem('theme', 'dark');
        } else {
            root.classList.remove('dark');
            localStorage.setItem('theme', 'light');
        }
    }, [darkMode]);

    const toggleTheme = () => setDarkMode(prev => !prev);

    return { darkMode, toggleTheme };
}

export default useTheme;
