"use client";

import { useEffect, useRef } from 'react';
import { siteConfig } from '../siteConfig';

// 静态站点评论区（灵境专用）：Giscus，无需服务器代理
export default function LabComments({ pageId }: { pageId?: string }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const cfg = (siteConfig as any).giscusConfig;

  useEffect(() => {
    if (!cfg?.repo || !cfg?.repoId || !cfg?.categoryId || !containerRef.current) return;
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
    s.setAttribute('data-term', pageId || 'workshop');
    s.setAttribute('data-strict', '0');
    s.setAttribute('data-reactions-enabled', '1');
    s.setAttribute('data-emit-metadata', '0');
    s.setAttribute('data-input-position', 'bottom');
    s.setAttribute('data-theme', 'preferred_color_scheme');
    s.setAttribute('data-lang', 'zh-CN');
    s.setAttribute('data-loading', 'lazy');
    containerRef.current.appendChild(s);
  }, [pageId, cfg?.repo, cfg?.repoId]);

  return (
    <div ref={containerRef} className="w-full mt-8 relative z-10" />
  );
}
