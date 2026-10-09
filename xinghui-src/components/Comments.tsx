"use client";

import { useEffect, useRef, useState } from 'react';
import { usePathname } from 'next/navigation';
import { siteConfig } from '../siteConfig';

// 静态站点评论区：使用 Giscus（GitHub Discussions 后端，无需服务器代理）
export default function Comments() {
  const containerRef = useRef<HTMLDivElement>(null);
  const pathname = usePathname();
  const [enabled, setEnabled] = useState(false);

  const cfg = (siteConfig as any).giscusConfig;

  useEffect(() => {
    if (!cfg?.repo || !cfg?.repoId || !cfg?.categoryId) return;
    if (!containerRef.current) return;

    containerRef.current.innerHTML = '';
    const s = document.createElement('script');
    s.src = 'https://giscus.app/client.js';
    s.async = true;
    s.crossOrigin = 'anonymous';
    s.setAttribute('data-repo', cfg.repo);
    s.setAttribute('data-repo-id', cfg.repoId);
    s.setAttribute('data-category', cfg.category || 'Announcements');
    s.setAttribute('data-category-id', cfg.categoryId || '');
    s.setAttribute('data-mapping', 'specific');
    s.setAttribute('data-term', (pathname.replace(/\/$/, '') || '/'));
    s.setAttribute('data-strict', '0');
    s.setAttribute('data-reactions-enabled', '1');
    s.setAttribute('data-emit-metadata', '0');
    s.setAttribute('data-input-position', 'bottom');
    s.setAttribute('data-theme', 'preferred_color_scheme');
    s.setAttribute('data-lang', 'zh-CN');
    s.setAttribute('data-loading', 'lazy');
    containerRef.current.appendChild(s);
    setEnabled(true);
  }, [pathname, cfg?.repo, cfg?.repoId]);

  return (
    <div className="w-full mt-16 relative">
      <div className="absolute -top-10 left-1/2 -translate-x-1/2 w-3/4 h-32 bg-indigo-500/10 dark:bg-indigo-500/20 blur-3xl rounded-full pointer-events-none z-0"></div>

      <h3 className="relative z-10 text-lg font-black text-slate-800 dark:text-white mb-4 tracking-wider">
        💬 留言讨论
      </h3>

      <div ref={containerRef} className="relative z-10 pt-2" />

      {!cfg?.categoryId && (
        <p className="relative z-10 text-sm text-slate-500 dark:text-slate-400">
          评论区未启用（配置 siteConfig.giscusConfig 后即可显示）
        </p>
      )}
    </div>
  );
}
