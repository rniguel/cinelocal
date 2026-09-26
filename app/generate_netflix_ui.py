# -*- coding: utf-8 -*-
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(APP_DIR, "index.html")

html_content = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>CineLocal - Home Theater & Streaming</title>
  <style>
    :root {
      --bg-dark: #090b10;
      --bg-card: #131722;
      --bg-card-hover: #1c2233;
      --bg-surface: #171c2a;
      --primary: #e50914;
      --primary-hover: #f40612;
      --accent: #6366f1;
      --gold: #f5c518;
      --vlc-orange: #ff8800;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --border: rgba(255, 255, 255, 0.08);
      --border-focus: rgba(229, 9, 20, 0.6);
      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 18px;
      --shadow-sm: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
      --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.7);
      --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
      -webkit-font-smoothing: antialiased;
    }

    body {
      background-color: var(--bg-dark);
      color: var(--text-main);
      font-family: var(--font-family);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
      padding-bottom: env(safe-area-inset-bottom);
    }

    /* HEADER NETFLIX */
    header {
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(9, 11, 16, 0.95);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border-bottom: 1px solid var(--border);
      padding: 12px 28px;
      transition: background 0.3s;
    }

    .header-content {
      max-width: 1700px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 20px;
    }

    .header-left {
      display: flex;
      align-items: center;
      gap: 32px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
      text-decoration: none;
      color: inherit;
    }

    .brand-icon {
      width: 38px;
      height: 38px;
      background: linear-gradient(135deg, var(--primary), #880008);
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 16px rgba(229, 9, 20, 0.45);
      flex-shrink: 0;
    }

    .brand-title {
      font-size: 22px;
      font-weight: 900;
      letter-spacing: -0.5px;
      background: linear-gradient(to right, #ffffff, #cbd5e1);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .brand-badge {
      font-size: 10px;
      text-transform: uppercase;
      font-weight: 800;
      background: rgba(229, 9, 20, 0.2);
      color: var(--primary);
      padding: 2px 7px;
      border-radius: 4px;
      border: 1px solid rgba(229, 9, 20, 0.3);
      letter-spacing: 0.5px;
    }

    /* NAV LINKS */
    .main-nav {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .nav-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 15px;
      font-weight: 600;
      padding: 8px 14px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .nav-btn:hover {
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.05);
    }

    .nav-btn.active {
      color: #fff;
      background: rgba(229, 9, 20, 0.15);
      border: 1px solid rgba(229, 9, 20, 0.3);
    }

    .header-right {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    /* SEARCH BAR NO HEADER */
    .search-container {
      position: relative;
      display: flex;
      align-items: center;
    }

    .search-input {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--border);
      color: #fff;
      padding: 9px 14px 9px 38px;
      border-radius: 20px;
      font-size: 14px;
      width: 260px;
      outline: none;
      transition: all 0.25s ease;
    }

    .search-input:focus {
      width: 320px;
      background: rgba(23, 28, 42, 0.95);
      border-color: var(--border-focus);
      box-shadow: 0 0 14px rgba(229, 9, 20, 0.25);
    }

    .search-icon {
      position: absolute;
      left: 12px;
      color: var(--text-muted);
      pointer-events: none;
    }

    .search-clear {
      position: absolute;
      right: 12px;
      background: none;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 16px;
      display: none;
    }

    .badge-protocol {
      font-size: 11px;
      font-weight: 700;
      padding: 5px 10px;
      border-radius: 20px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .badge-lan {
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .badge-local {
      background: rgba(99, 102, 241, 0.15);
      color: #818cf8;
      border: 1px solid rgba(99, 102, 241, 0.3);
    }

    .btn-header-action {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 7px 12px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 13px;
      font-weight: 600;
      transition: all 0.2s;
    }

    .btn-header-action:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.12);
    }

    /* HERO BANNER WIDESCREEN */
    .hero-banner {
      position: relative;
      width: 100%;
      height: 520px;
      display: flex;
      align-items: flex-end;
      padding: 40px 60px;
      box-sizing: border-box;
      background-size: cover;
      background-position: center 25%;
      overflow: hidden;
      margin-bottom: 20px;
      transition: background-image 0.8s ease-in-out;
    }

    .hero-backdrop-gradient {
      position: absolute;
      inset: 0;
      background: linear-gradient(to top, var(--bg-dark) 5%, rgba(9, 11, 16, 0.7) 45%, rgba(9, 11, 16, 0.2) 100%),
                  linear-gradient(to right, rgba(9, 11, 16, 0.95) 15%, rgba(9, 11, 16, 0.6) 45%, transparent 100%);
      pointer-events: none;
    }

    .hero-content {
      position: relative;
      z-index: 2;
      max-width: 680px;
      animation: fadeIn 0.6s ease;
    }

    .hero-badge-tag {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 1px;
      text-transform: uppercase;
      background: var(--primary);
      color: #fff;
      padding: 4px 10px;
      border-radius: 4px;
      margin-bottom: 12px;
      box-shadow: 0 2px 8px rgba(229, 9, 20, 0.5);
    }

    .hero-title {
      font-size: 42px;
      font-weight: 900;
      line-height: 1.1;
      margin-bottom: 12px;
      letter-spacing: -1px;
      text-shadow: 0 4px 12px rgba(0, 0, 0, 0.8);
    }

    .hero-meta {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 14px;
      color: var(--text-muted);
      margin-bottom: 14px;
      font-weight: 600;
    }

    .hero-meta .badge-res {
      background: rgba(255, 255, 255, 0.15);
      color: #fff;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 700;
    }

    .hero-overview {
      font-size: 15px;
      line-height: 1.5;
      color: #cbd5e1;
      margin-bottom: 24px;
      text-shadow: 0 2px 4px rgba(0, 0, 0, 0.6);
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .hero-buttons {
      display: flex;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
    }

    .btn-hero-play {
      background: #fff;
      color: #000;
      border: none;
      padding: 12px 28px;
      border-radius: var(--radius-sm);
      font-size: 16px;
      font-weight: 800;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 10px;
      transition: all 0.2s ease;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.5);
    }

    .btn-hero-play:hover {
      background: rgba(255, 255, 255, 0.85);
      transform: scale(1.03);
    }

    .btn-hero-vlc {
      background: rgba(255, 136, 0, 0.2);
      border: 1px solid rgba(255, 136, 0, 0.5);
      color: #ff9922;
      padding: 12px 22px;
      border-radius: var(--radius-sm);
      font-size: 15px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
      backdrop-filter: blur(10px);
    }

    .btn-hero-vlc:hover {
      background: rgba(255, 136, 0, 0.35);
      color: #fff;
      transform: scale(1.03);
    }

    .btn-hero-info {
      background: rgba(100, 116, 139, 0.3);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #fff;
      padding: 12px 20px;
      border-radius: var(--radius-sm);
      font-size: 15px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
      backdrop-filter: blur(10px);
    }

    .btn-hero-info:hover {
      background: rgba(100, 116, 139, 0.5);
    }

    /* CARROSSEL NETFLIX (TRILHOS HORIZONTAIS) */
    .carousel-section {
      position: relative;
      margin-bottom: 34px;
      padding: 0 40px;
    }

    .carousel-header {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      margin-bottom: 14px;
    }

    .carousel-title-box {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .carousel-title {
      font-size: 20px;
      font-weight: 800;
      letter-spacing: -0.3px;
      color: #fff;
    }

    .carousel-count {
      font-size: 12px;
      color: var(--text-muted);
      font-weight: 600;
    }

    .carousel-track-wrapper {
      position: relative;
    }

    .carousel-track {
      display: flex;
      gap: 16px;
      overflow-x: auto;
      overflow-y: hidden;
      scroll-behavior: smooth;
      padding: 12px 4px 20px 4px;
      scrollbar-width: none;
      -ms-overflow-style: none;
    }

    .carousel-track::-webkit-scrollbar {
      display: none;
    }

    .carousel-btn {
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      width: 44px;
      height: 70px;
      background: rgba(9, 11, 16, 0.8);
      border: 1px solid var(--border);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      z-index: 10;
      border-radius: var(--radius-sm);
      opacity: 0;
      transition: all 0.25s ease;
      backdrop-filter: blur(8px);
    }

    .carousel-track-wrapper:hover .carousel-btn {
      opacity: 1;
    }

    .carousel-btn:hover {
      background: rgba(229, 9, 20, 0.85);
      border-color: var(--primary);
      transform: translateY(-50%) scale(1.08);
    }

    .carousel-btn.left {
      left: -20px;
    }

    .carousel-btn.right {
      right: -20px;
    }

    /* CARDS DE MÍDIA */
    .movie-card {
      flex: 0 0 190px;
      width: 190px;
      border-radius: var(--radius-md);
      background: var(--bg-card);
      border: 1px solid var(--border);
      overflow: hidden;
      cursor: pointer;
      position: relative;
      transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
      display: flex;
      flex-direction: column;
    }

    .movie-card:hover {
      transform: translateY(-8px) scale(1.04);
      border-color: rgba(229, 9, 20, 0.6);
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.8), 0 0 16px rgba(229, 9, 20, 0.3);
      z-index: 5;
    }

    .card-poster-wrapper {
      position: relative;
      width: 100%;
      aspect-ratio: 2 / 3;
      background: #111520;
      overflow: hidden;
    }

    .card-poster {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.4s ease;
    }

    .movie-card:hover .card-poster {
      transform: scale(1.06);
    }

    .card-badge {
      position: absolute;
      top: 8px;
      left: 8px;
      padding: 3px 7px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      backdrop-filter: blur(8px);
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.5);
    }

    .badge-4k {
      background: rgba(245, 197, 24, 0.9);
      color: #000;
    }

    .badge-1080p {
      background: rgba(37, 99, 235, 0.85);
      color: #fff;
    }

    .badge-720p {
      background: rgba(100, 116, 139, 0.85);
      color: #fff;
    }

    .badge-series {
      background: linear-gradient(135deg, #e50914, #990008);
      color: #fff;
    }

    .badge-seq {
      position: absolute;
      top: 8px;
      right: 8px;
      background: rgba(0, 0, 0, 0.8);
      color: #fff;
      font-size: 11px;
      font-weight: 800;
      padding: 3px 7px;
      border-radius: 4px;
      border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .card-tag-group {
      position: absolute;
      bottom: 8px;
      left: 8px;
      display: flex;
      gap: 4px;
      z-index: 2;
    }

    .badge-tag {
      font-size: 10px;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 4px;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      backdrop-filter: blur(8px);
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.6);
      line-height: 1.2;
    }

    .badge-dual {
      background: rgba(14, 165, 233, 0.9);
      color: #ffffff;
      border: 1px solid rgba(56, 189, 248, 0.4);
    }

    .badge-dub {
      background: rgba(16, 185, 129, 0.9);
      color: #ffffff;
      border: 1px solid rgba(52, 211, 153, 0.4);
    }

    .badge-leg {
      background: rgba(139, 92, 246, 0.9);
      color: #ffffff;
      border: 1px solid rgba(167, 139, 250, 0.4);
    }

    .badge-sub {
      background: rgba(245, 158, 11, 0.95);
      color: #000000;
      font-weight: 900;
      border: 1px solid rgba(251, 191, 36, 0.8);
    }

    /* CONTROLE DE VOLUME NO PLAYER */
    .volume-container {
      display: flex;
      align-items: center;
      gap: 6px;
      margin: 0 4px;
    }

    .volume-slider-box {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .volume-slider {
      -webkit-appearance: none;
      width: 76px;
      height: 5px;
      border-radius: 4px;
      background: #334155;
      outline: none;
      cursor: pointer;
      accent-color: var(--primary);
      transition: background 0.2s ease;
    }

    .volume-slider::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      width: 13px;
      height: 13px;
      border-radius: 50%;
      background: #ffffff;
      cursor: pointer;
      box-shadow: 0 1px 4px rgba(0,0,0,0.5);
    }

    .volume-slider.boosted {
      accent-color: #f97316;
      background: linear-gradient(to right, var(--primary) 33%, #f97316 66%, #ef4444 100%);
    }

    .volume-percent {
      font-size: 11px;
      font-weight: 800;
      color: var(--text-muted);
      min-width: 44px;
      cursor: pointer;
      user-select: none;
      transition: color 0.2s ease;
    }

    .volume-percent.boosted {
      color: #f97316;
      text-shadow: 0 0 8px rgba(249, 115, 22, 0.4);
    }

    .card-content {
      padding: 12px;
      display: flex;
      flex-direction: column;
      flex: 1;
      justify-content: space-between;
    }

    .card-title {
      font-size: 14px;
      font-weight: 700;
      color: #fff;
      line-height: 1.3;
      margin-bottom: 4px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .card-subinfo {
      font-size: 12px;
      color: var(--text-muted);
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .card-actions {
      display: flex;
      align-items: center;
      gap: 6px;
      margin-top: 6px;
    }

    .card-btn-play {
      flex: 1;
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid var(--border);
      color: #fff;
      padding: 6px 8px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      transition: all 0.2s;
    }

    .card-btn-play:hover {
      background: var(--primary);
      border-color: var(--primary);
    }

    .card-btn-vlc {
      background: rgba(255, 136, 0, 0.15);
      border: 1px solid rgba(255, 136, 0, 0.35);
      color: #ff9922;
      padding: 6px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      transition: all 0.2s;
    }

    .card-btn-vlc:hover {
      background: var(--vlc-orange);
      color: #fff;
    }

    /* GRID VIEW (FILMES E SÉRIES DEDICADAS) */
    .view-container {
      max-width: 1700px;
      margin: 0 auto;
      padding: 24px 40px;
      width: 100%;
    }

    .view-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 24px;
      flex-wrap: wrap;
      gap: 16px;
    }

    .view-title-group h2 {
      font-size: 28px;
      font-weight: 900;
      letter-spacing: -0.5px;
    }

    .view-title-group p {
      font-size: 14px;
      color: var(--text-muted);
      margin-top: 4px;
    }

    .filter-chips {
      display: flex;
      align-items: center;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 8px;
      margin-bottom: 20px;
    }

    .chip {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 7px 14px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s;
    }

    .chip:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.12);
    }

    .chip.active {
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
      box-shadow: 0 0 10px rgba(229, 9, 20, 0.4);
    }

    /* SELECTS DE FILTROS MODERNOS (GÊNERO E ANO) */
    .filter-select {
      appearance: none;
      -webkit-appearance: none;
      -moz-appearance: none;
      background-color: #171c2a;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23cbd5e1' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
      background-repeat: no-repeat;
      background-position: right 14px center;
      background-size: 11px;
      padding: 7px 34px 7px 14px;
      border: 1px solid var(--border);
      border-radius: 20px;
      color: #f8fafc;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      outline: none;
      color-scheme: dark;
      transition: all 0.2s ease;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.25);
    }

    .filter-select:hover {
      border-color: rgba(255, 255, 255, 0.3);
      background-color: #1e2436;
      color: #fff;
    }

    .filter-select:focus,
    .filter-select:focus-visible {
      border-color: var(--primary);
      box-shadow: 0 0 0 2px rgba(229, 9, 20, 0.35);
    }

    .filter-select option {
      background-color: #131722 !important;
      color: #f8fafc !important;
      padding: 10px 14px;
      font-size: 14px;
      font-weight: 500;
    }

    .filter-select option:checked {
      background-color: #e50914 !important;
      color: #ffffff !important;
    }

    .card-btn-fav {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #cbd5e1;
      padding: 4px 7px;
      cursor: pointer;
      font-size: 13px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      transition: all 0.15s ease;
    }
    .card-btn-fav:hover {
      background: rgba(255, 255, 255, 0.2);
      color: #f59e0b;
      transform: scale(1.1);
    }
    .btn-vlc-secondary.active {
      background: rgba(245, 158, 11, 0.2) !important;
      border-color: #f59e0b !important;
      color: #f59e0b !important;
    }
    .qr-tab-bar {
      display: flex;
      gap: 8px;
      justify-content: center;
      margin-bottom: 16px;
    }
    .qr-tab-btn {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 7px 16px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .qr-tab-btn.active {
      background: var(--primary);
      border-color: var(--primary);
      color: #fff;
    }

    .grid-layout {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(185px, 1fr));
      gap: 20px;
    }

    /* MODAL DE SÉRIE ESTILO NETFLIX */
    .series-modal {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.85);
      backdrop-filter: blur(12px);
      z-index: 150;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
      opacity: 0;
      transition: opacity 0.3s ease;
    }

    .series-modal.active {
      display: flex;
      opacity: 1;
    }

    .series-modal-box {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      width: 100%;
      max-width: 900px;
      max-height: 90vh;
      overflow-y: auto;
      position: relative;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.9);
      animation: modalSlideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    @keyframes modalSlideUp {
      from { transform: translateY(30px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }

    .series-modal-header {
      position: relative;
      padding: 30px;
      display: flex;
      gap: 24px;
      background: linear-gradient(to bottom, rgba(23, 28, 42, 0.8), var(--bg-card));
      border-bottom: 1px solid var(--border);
    }

    .series-modal-close {
      position: absolute;
      top: 16px;
      right: 16px;
      width: 36px;
      height: 36px;
      background: rgba(0, 0, 0, 0.6);
      border: 1px solid var(--border);
      color: #fff;
      border-radius: 50%;
      font-size: 20px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s;
      z-index: 5;
    }

    .series-modal-close:hover {
      background: var(--primary);
    }

    .series-modal-poster {
      width: 160px;
      aspect-ratio: 2 / 3;
      border-radius: var(--radius-md);
      object-fit: cover;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.6);
      flex-shrink: 0;
    }

    .series-modal-info {
      display: flex;
      flex-direction: column;
      justify-content: center;
    }

    .series-modal-title {
      font-size: 32px;
      font-weight: 900;
      color: #fff;
      margin-bottom: 8px;
    }

    .series-modal-meta {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
      font-size: 13px;
      color: var(--text-muted);
      margin-bottom: 10px;
    }

    .rating-badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: rgba(245, 197, 24, 0.2);
      color: #f5c518;
      border: 1px solid rgba(245, 197, 24, 0.4);
      font-weight: 800;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 12px;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
    }

    .modal-genres-row {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 12px;
    }

    .genre-pill {
      background: rgba(255, 255, 255, 0.08);
      color: #e2e8f0;
      border: 1px solid rgba(255, 255, 255, 0.15);
      font-size: 11px;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: 12px;
    }

    .series-modal-desc {
      font-size: 14px;
      line-height: 1.6;
      color: #cbd5e1;
      margin-bottom: 12px;
    }

    .modal-credits {
      padding-top: 10px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      font-size: 13px;
      color: #94a3b8;
      display: flex;
      flex-direction: column;
      gap: 4px;
      margin-bottom: 12px;
    }

    .modal-credits strong {
      color: #e2e8f0;
    }

    .modal-links-row {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 8px;
    }

    .btn-external-link {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #cbd5e1;
      padding: 5px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      text-decoration: none;
      transition: all 0.2s;
    }

    .btn-external-link:hover {
      background: rgba(255, 255, 255, 0.15);
      color: #fff;
    }

    .btn-external-link.tmdb:hover {
      border-color: #01b4e4;
      color: #01b4e4;
    }

    .btn-external-link.imdb:hover {
      border-color: #f5c518;
      color: #f5c518;
    }

    .movie-modal-actions {
      display: flex;
      gap: 10px;
      margin-top: 14px;
    }

    .btn-play-primary {
      background: var(--primary);
      color: #fff;
      border: none;
      padding: 10px 18px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }

    .btn-play-primary:hover {
      background: #ff1f2d;
      transform: translateY(-2px);
      box-shadow: 0 4px 14px rgba(229, 9, 20, 0.4);
    }

    .btn-vlc-secondary {
      background: rgba(255, 136, 0, 0.18);
      color: #ff9922;
      border: 1px solid rgba(255, 136, 0, 0.4);
      padding: 10px 16px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }

    .btn-vlc-secondary:hover {
      background: var(--vlc-orange);
      color: #fff;
      transform: translateY(-2px);
      box-shadow: 0 4px 14px rgba(255, 136, 0, 0.4);
    }

    .card-btn-info {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #94a3b8;
      padding: 6px 10px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 800;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s;
    }

    .card-btn-info:hover {
      background: rgba(255, 255, 255, 0.2);
      color: #fff;
      border-color: #fff;
    }

    .series-seasons-tabs {
      display: flex;
      gap: 10px;
      padding: 16px 30px;
      border-bottom: 1px solid var(--border);
      background: rgba(0, 0, 0, 0.2);
    }

    .season-tab {
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 6px 14px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
    }

    .season-tab.active {
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
    }

    .series-episodes-list {
      padding: 20px 30px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .episode-card {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 14px 18px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      transition: all 0.2s;
      cursor: pointer;
    }

    .episode-card:hover {
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(229, 9, 20, 0.4);
      transform: translateX(4px);
    }

    .episode-left {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .episode-num {
      font-size: 16px;
      font-weight: 800;
      color: var(--text-muted);
      width: 32px;
    }

    .episode-title-box h4 {
      font-size: 15px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 4px;
    }

    .episode-title-box p {
      font-size: 12px;
      color: var(--text-muted);
    }

    .episode-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    /* CINEMA PLAYER */
    .player-modal {
      position: fixed;
      inset: 0;
      background: #000;
      z-index: 200;
      display: none;
      flex-direction: column;
    }

    .player-modal.active {
      display: flex;
    }

    .player-container {
      position: relative;
      width: 100%;
      height: 100%;
      background: #000;
      display: flex;
      flex-direction: column;
    }

    .player-top-bar {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      padding: 16px 24px;
      background: linear-gradient(to bottom, rgba(0, 0, 0, 0.9), transparent);
      z-index: 10;
      display: flex;
      align-items: center;
      justify-content: space-between;
      transition: opacity 0.3s;
    }

    .player-back-btn {
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #fff;
      padding: 8px 14px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 14px;
      font-weight: 700;
    }

    .player-movie-heading {
      text-align: center;
    }

    .player-movie-title {
      font-size: 18px;
      font-weight: 800;
      color: #fff;
    }

    .player-movie-sub {
      font-size: 12px;
      color: var(--text-muted);
    }

    .video-viewport {
      position: relative;
      flex: 1;
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #000;
    }

    video {
      width: 100%;
      height: 100%;
      object-fit: contain;
    }

    .subtitle-display {
      position: absolute;
      bottom: 120px;
      left: 50%;
      transform: translateX(-50%);
      text-align: center;
      max-width: 88%;
      pointer-events: none;
      z-index: 40;
      transition: bottom 0.25s ease-out;
    }

    .player-container.controls-hidden .subtitle-display {
      bottom: 45px;
    }

    .subtitle-text {
      background: rgba(0, 0, 0, 0.82);
      color: #ffffff;
      padding: 8px 18px;
      border-radius: 8px;
      font-size: 24px;
      line-height: 1.4;
      font-weight: 600;
      text-shadow: 0 2px 4px rgba(0, 0, 0, 0.9);
      white-space: pre-line;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.12);
    }

    .subtitle-display.size-sm .subtitle-text { font-size: 18px; padding: 6px 14px; }
    .subtitle-display.size-md .subtitle-text { font-size: 24px; padding: 8px 18px; }
    .subtitle-display.size-lg .subtitle-text { font-size: 30px; padding: 10px 22px; }
    .subtitle-display.size-xl .subtitle-text { font-size: 38px; padding: 12px 26px; }

    .player-bottom-controls {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      padding: 16px 24px 20px 24px;
      background: linear-gradient(to top, rgba(0, 0, 0, 0.95), transparent);
      z-index: 10;
      display: flex;
      flex-direction: column;
      gap: 10px;
      transition: opacity 0.3s;
    }

    .player-container.controls-hidden .player-top-bar,
    .player-container.controls-hidden .player-bottom-controls {
      opacity: 0;
      pointer-events: none;
    }

    .seek-bar-container {
      position: relative;
      width: 100%;
      height: 8px;
      background: rgba(255, 255, 255, 0.2);
      border-radius: 4px;
      cursor: pointer;
    }

    .seek-bar-track {
      position: relative;
      width: 100%;
      height: 100%;
      border-radius: 4px;
      overflow: hidden;
    }

    .seek-bar-buffered {
      position: absolute;
      top: 0;
      left: 0;
      height: 100%;
      background: rgba(255, 255, 255, 0.4);
      width: 0%;
    }

    .seek-bar-fill {
      position: absolute;
      top: 0;
      left: 0;
      height: 100%;
      background: var(--primary);
      width: 0%;
    }

    .controls-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .controls-left, .controls-right {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .btn-ctrl {
      background: transparent;
      border: none;
      color: #fff;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 6px;
      border-radius: 4px;
      transition: all 0.2s;
    }

    .btn-ctrl:hover {
      color: var(--primary);
      transform: scale(1.1);
    }

    .time-display {
      font-size: 13px;
      font-weight: 600;
      color: #cbd5e1;
      font-variant-numeric: tabular-nums;
    }

    .dropdown {
      position: relative;
    }

    .dropdown-menu {
      position: absolute;
      bottom: 45px;
      right: 0;
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 10px;
      min-width: 220px;
      display: none;
      flex-direction: column;
      gap: 6px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.8);
      z-index: 20;
    }

    .dropdown-menu.active {
      display: flex;
    }

    .dropdown-item {
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 8px 12px;
      border-radius: 4px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      text-align: left;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .dropdown-item:hover, .dropdown-item.active {
      background: rgba(229, 9, 20, 0.15);
      color: #fff;
    }

    /* TOAST */
    .toast-container {
      position: fixed;
      bottom: 30px;
      right: 30px;
      z-index: 300;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .toast {
      background: rgba(19, 23, 34, 0.95);
      border: 1px solid rgba(229, 9, 20, 0.5);
      color: #fff;
      padding: 12px 20px;
      border-radius: var(--radius-sm);
      font-size: 14px;
      font-weight: 600;
      box-shadow: 0 10px 20px rgba(0, 0, 0, 0.6);
      animation: fadeIn 0.3s ease;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* CURSOR OCULTO EM FULLSCREEN */
    .player-container.controls-hidden {
      cursor: none;
    }

    /* PULSO CENTRAL DE PLAY / PAUSE (ESTILO YOUTUBE) */
    .player-center-feedback {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      pointer-events: none;
      z-index: 50;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .feedback-bubble {
      width: 80px;
      height: 80px;
      border-radius: 50%;
      background: rgba(0, 0, 0, 0.75);
      border: 2px solid rgba(255, 255, 255, 0.3);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      animation: fbPulse 0.55s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    @keyframes fbPulse {
      0% { transform: scale(0.6); opacity: 0; }
      50% { transform: scale(1.15); opacity: 1; }
      100% { transform: scale(1.35); opacity: 0; }
    }

    /* BARRA DE PROGRESSO NO CARD ("CONTINUAR ASSISTINDO") */
    .card-progress-bar {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: rgba(255, 255, 255, 0.25);
      overflow: hidden;
      z-index: 5;
    }
    .card-progress-fill {
      height: 100%;
      background: var(--primary);
      transition: width 0.3s;
    }
    .card-watched-badge {
      position: absolute;
      top: 8px;
      left: 8px;
      background: rgba(16, 185, 129, 0.92);
      color: #fff;
      font-size: 10px;
      font-weight: 800;
      padding: 2px 7px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      gap: 3px;
      z-index: 6;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.6);
      backdrop-filter: blur(4px);
    }
    .btn-watched-toggle {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .btn-watched-toggle:hover {
      background: rgba(255, 255, 255, 0.15);
      color: #fff;
    }
    .btn-watched-toggle.active {
      background: rgba(16, 185, 129, 0.2);
      border-color: #10b981;
      color: #10b981;
    }

    /* PRÓXIMO EPISÓDIO AUTOMÁTICO (COUNTDOWN TOAST) */
    .next-episode-toast {
      position: absolute;
      bottom: 95px;
      right: 28px;
      background: rgba(18, 22, 34, 0.96);
      border: 1px solid rgba(229, 9, 20, 0.55);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8), 0 0 20px rgba(229, 9, 20, 0.35);
      border-radius: 10px;
      padding: 12px 18px;
      display: flex;
      align-items: center;
      gap: 14px;
      z-index: 60;
      backdrop-filter: blur(10px);
      animation: slideInRight 0.35s ease-out;
    }
    @keyframes slideInRight {
      from { transform: translateX(40px); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }
    .next-ep-content {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    .next-ep-badge {
      font-size: 11px;
      font-weight: 700;
      color: #ffb4b4;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .next-ep-name {
      font-size: 14px;
      font-weight: 800;
      color: #fff;
      max-width: 240px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .btn-next-play {
      background: var(--primary);
      color: #fff;
      border: none;
      border-radius: 6px;
      padding: 7px 14px;
      font-size: 12px;
      font-weight: 800;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: transform 0.2s, background 0.2s;
    }
    .btn-next-play:hover {
      background: #b20710;
      transform: scale(1.05);
    }
    .btn-next-cancel {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 18px;
      cursor: pointer;
      padding: 4px;
      line-height: 1;
    }
    .btn-next-cancel:hover {
      color: #fff;
    }

    /* FOCO D-PAD PARA SMART TV / CONTROLE REMOTO */
    :focus-visible {
      outline: 3px solid var(--primary) !important;
      outline-offset: 3px !important;
    }
    .movie-card:focus-visible,
    .movie-card.tv-focused {
      outline: 3px solid #e50914 !important;
      outline-offset: 4px !important;
      transform: scale(1.08) translateY(-4px) !important;
      z-index: 20 !important;
      box-shadow: 0 10px 30px rgba(229, 9, 20, 0.6) !important;
    }

    /* MODAL QR CODE E MODAL SURPREENDA-ME */
    .qr-modal-box {
      max-width: 480px !important;
      text-align: center;
      padding: 28px;
    }
    .qr-container-box {
      background: #fff;
      padding: 16px;
      border-radius: 12px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
      margin: 16px 0;
    }
    .surprise-card-box {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px;
      display: flex;
      gap: 16px;
      align-items: center;
      text-align: left;
    }
    .surprise-poster {
      width: 90px;
      height: 135px;
      object-fit: cover;
      border-radius: 6px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }

    @media (max-width: 768px) {
      header { padding: 12px 16px; }
      .hero-banner { height: 420px; padding: 24px 20px; }
      .hero-title { font-size: 28px; }
      .carousel-section { padding: 0 16px; }
      .search-input { width: 160px; }
      .search-input:focus { width: 200px; }
      .movie-card { flex: 0 0 145px; width: 145px; }
    }

    /* MCU TIMELINE & TRACKER STYLES */
    .btn-mcu-timeline-header {
      background: linear-gradient(135deg, rgba(229, 9, 20, 0.25), rgba(255, 59, 48, 0.15));
      border: 1px solid rgba(229, 9, 20, 0.45);
      color: #fff;
      padding: 7px 14px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 7px;
      transition: all 0.25s ease;
    }
    .btn-mcu-timeline-header:hover {
      background: linear-gradient(135deg, #e50914, #ff3b30);
      transform: translateY(-2px);
      box-shadow: 0 4px 14px rgba(229, 9, 20, 0.5);
    }
    .pulse-dot {
      width: 7px;
      height: 7px;
      background: #00ff88;
      border-radius: 50%;
      box-shadow: 0 0 8px #00ff88;
      animation: pulseAnim 1.8s infinite;
    }
    @keyframes pulseAnim {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.8); }
    }

    /* CARD DE DESTAQUE NO CARROSSEL MCU */
    .movie-card.mcu-hero-card {
      border: 1px solid rgba(229, 9, 20, 0.45);
      background: linear-gradient(160deg, #220a10 0%, #10141f 100%);
      cursor: pointer;
    }
    .movie-card.mcu-hero-card:hover {
      border-color: #e50914;
      box-shadow: 0 10px 25px rgba(229, 9, 20, 0.4);
      transform: translateY(-6px) scale(1.02);
    }
    .mcu-poster-wrapper {
      background: radial-gradient(circle at 50% 30%, #520912 0%, #120508 100%) !important;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .mcu-card-inner {
      width: 100%;
      height: 100%;
      padding: 16px 12px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      text-align: center;
      box-sizing: border-box;
    }
    .mcu-badge-top {
      font-size: 9px;
      font-weight: 800;
      letter-spacing: 1.2px;
      color: #ffb4b4;
      background: rgba(229, 9, 20, 0.4);
      padding: 3px 8px;
      border-radius: 4px;
      text-transform: uppercase;
    }
    .mcu-marvel-logo {
      background: #e50914;
      color: #fff;
      font-weight: 900;
      letter-spacing: 2px;
      font-size: 19px;
      padding: 3px 10px;
      font-family: Impact, 'Arial Black', sans-serif;
      box-shadow: 0 4px 12px rgba(229, 9, 20, 0.6);
      margin-top: 6px;
    }
    .mcu-icon-orb {
      font-size: 30px;
      filter: drop-shadow(0 0 12px rgba(255, 215, 0, 0.7));
      margin: 4px 0;
    }
    .mcu-stats-mini {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 2px;
    }
    .mcu-stat-num {
      font-size: 18px;
      font-weight: 800;
      color: #00ff88;
      text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
    }
    .mcu-stat-lbl {
      font-size: 11px;
      color: var(--text-muted);
      font-weight: 600;
    }
    .mcu-progress-container {
      width: 100%;
      height: 6px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 3px;
      overflow: hidden;
      margin-top: 6px;
    }
    .mcu-progress-bar {
      height: 100%;
      background: linear-gradient(90deg, #e50914, #00ff88);
      border-radius: 3px;
      transition: width 0.4s ease;
    }
    .mcu-btn-play {
      background: linear-gradient(135deg, #e50914, #b20710) !important;
      font-size: 11px !important;
      font-weight: 800 !important;
      width: 100%;
      justify-content: center;
    }

    /* MODAL DO RASTREADOR DO MCU */
    .mcu-modal-box {
      background: #10141f;
      border: 1px solid rgba(229, 9, 20, 0.4);
      border-radius: 14px;
      max-width: 960px;
      width: 95%;
      max-height: 90vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      position: relative;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8), 0 0 35px rgba(229, 9, 20, 0.25);
    }
    .mcu-modal-header {
      padding: 22px 26px 16px;
      background: linear-gradient(180deg, #1f0b12 0%, #10141f 100%);
      border-bottom: 1px solid var(--border);
    }
    .mcu-header-brand-row {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 8px;
    }
    .mcu-studios-tag {
      background: #e50914;
      color: #fff;
      font-family: Impact, 'Arial Black', sans-serif;
      font-size: 14px;
      letter-spacing: 2px;
      padding: 3px 8px;
      border-radius: 3px;
    }
    .mcu-modal-title {
      font-size: 21px;
      font-weight: 800;
      color: #fff;
      margin: 0;
    }
    .mcu-modal-subtitle {
      font-size: 13px;
      color: var(--text-muted);
      margin: 4px 0 0;
    }
    .mcu-stats-dashboard {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      margin-top: 14px;
    }
    .mcu-stat-card {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px 14px;
      text-align: center;
    }
    .mcu-stat-card-val {
      font-size: 22px;
      font-weight: 800;
      color: #fff;
    }
    .mcu-stat-card-val.accent {
      color: #00ff88;
    }
    .mcu-stat-card-lbl {
      font-size: 11px;
      color: var(--text-muted);
      margin-top: 2px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .mcu-progress-large {
      height: 8px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 4px;
      overflow: hidden;
      margin-top: 12px;
    }
    .mcu-progress-large-fill {
      height: 100%;
      background: linear-gradient(90deg, #e50914, #ff8c00, #00ff88);
      border-radius: 4px;
      transition: width 0.5s ease;
    }
    .mcu-controls-bar {
      padding: 14px 26px;
      background: rgba(13, 17, 26, 0.7);
      border-bottom: 1px solid var(--border);
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
      justify-content: space-between;
    }
    .mcu-search-box {
      flex: 1;
      min-width: 240px;
      position: relative;
    }
    .mcu-search-input {
      width: 100%;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border);
      color: #fff;
      padding: 8px 14px 8px 36px;
      border-radius: 20px;
      font-size: 13px;
      outline: none;
      box-sizing: border-box;
      transition: all 0.2s;
    }
    .mcu-search-input:focus {
      border-color: #e50914;
      background: rgba(255, 255, 255, 0.1);
    }
    .mcu-search-icon {
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      font-size: 14px;
      pointer-events: none;
    }
    .mcu-filter-chips {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
    }
    .mcu-chip {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 6px 12px;
      border-radius: 16px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }
    .mcu-chip:hover {
      color: #fff;
      border-color: rgba(255, 255, 255, 0.3);
    }
    .mcu-chip.active {
      background: rgba(229, 9, 20, 0.2);
      border-color: #e50914;
      color: #fff;
    }
    .mcu-timeline-body {
      padding: 16px 26px 26px;
      overflow-y: auto;
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .mcu-timeline-item {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 12px 16px;
      display: flex;
      align-items: center;
      gap: 16px;
      transition: all 0.2s ease;
    }
    .mcu-timeline-item:hover {
      background: rgba(255, 255, 255, 0.06);
      border-color: rgba(229, 9, 20, 0.4);
      transform: translateX(4px);
    }
    .mcu-timeline-item.downloaded {
      border-left: 4px solid #00ff88;
      background: rgba(0, 255, 136, 0.03);
    }
    .mcu-timeline-item.missing {
      opacity: 0.75;
    }
    .mcu-item-seq {
      font-size: 18px;
      font-weight: 800;
      color: var(--text-muted);
      min-width: 38px;
      text-align: center;
    }
    .mcu-timeline-item.downloaded .mcu-item-seq {
      color: #00ff88;
    }
    .mcu-item-info {
      flex: 1;
    }
    .mcu-item-title-row {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
    .mcu-item-title {
      font-size: 15px;
      font-weight: 700;
      color: #fff;
    }
    .mcu-item-year {
      font-size: 13px;
      color: var(--text-muted);
    }
    .mcu-type-badge {
      font-size: 10px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .mcu-type-badge.movie {
      background: rgba(30, 144, 255, 0.18);
      color: #38bdf8;
      border: 1px solid rgba(30, 144, 255, 0.3);
    }
    .mcu-type-badge.series {
      background: rgba(168, 85, 247, 0.18);
      color: #c084fc;
      border: 1px solid rgba(168, 85, 247, 0.3);
    }
    .mcu-item-note {
      font-size: 12px;
      color: #cbd5e1;
      margin-top: 4px;
      font-style: italic;
    }
    .mcu-item-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .mcu-status-tag {
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 20px;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      white-space: nowrap;
    }
    .mcu-status-tag.downloaded {
      background: rgba(0, 255, 136, 0.15);
      border: 1px solid rgba(0, 255, 136, 0.4);
      color: #00ff88;
    }
    .mcu-status-tag.missing {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: var(--text-muted);
    }
    .mcu-status-tag.future {
      background: rgba(234, 179, 8, 0.15);
      border: 1px solid rgba(234, 179, 8, 0.4);
      color: #facc15;
    }
    .btn-mcu-play {
      background: #e50914;
      color: #fff;
      border: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: all 0.2s;
      white-space: nowrap;
    }
    .btn-mcu-play:hover {
      background: #ff1f2d;
      transform: translateY(-1px);
      box-shadow: 0 3px 10px rgba(229, 9, 20, 0.4);
    }
    .btn-mcu-play.series {
      background: #7c3aed;
    }
    .btn-mcu-play.series:hover {
      background: #9333ea;
      box-shadow: 0 3px 10px rgba(147, 51, 234, 0.4);
    }
    @media (max-width: 768px) {
      .mcu-stats-dashboard { grid-template-columns: repeat(2, 1fr); }
      .mcu-timeline-item { flex-direction: column; align-items: flex-start; gap: 8px; }
      .mcu-item-actions { width: 100%; justify-content: space-between; }
    }

    /* TELA DE ONBOARDING / BOAS-VINDAS (CATÁLOGO VAZIO) */
    .onboarding-container {
      max-width: 1050px;
      margin: 40px auto 80px;
      padding: 0 20px;
      animation: fadeIn 0.4s ease-out;
    }

    .onboarding-hero {
      text-align: center;
      padding: 48px 24px 36px;
      background: linear-gradient(180deg, rgba(229, 9, 20, 0.12) 0%, rgba(19, 23, 34, 0.6) 100%);
      border: 1px solid rgba(229, 9, 20, 0.25);
      border-radius: var(--radius-lg);
      margin-bottom: 32px;
      box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.6);
      position: relative;
      overflow: hidden;
    }

    .onboarding-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 5px 14px;
      border-radius: 999px;
      background: rgba(229, 9, 20, 0.2);
      border: 1px solid rgba(229, 9, 20, 0.4);
      color: #ff4d4d;
      font-size: 0.8rem;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      margin-bottom: 16px;
    }

    .onboarding-title {
      font-size: 2.2rem;
      font-weight: 800;
      color: var(--text-main);
      margin-bottom: 12px;
      line-height: 1.2;
    }

    .onboarding-subtitle {
      font-size: 1.05rem;
      color: var(--text-muted);
      max-width: 650px;
      margin: 0 auto;
      line-height: 1.6;
    }

    .onboarding-steps {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 20px;
      margin-bottom: 36px;
    }

    .onboarding-card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      transition: transform 0.2s, border-color 0.2s;
    }

    .onboarding-card:hover {
      transform: translateY(-3px);
      border-color: rgba(255, 255, 255, 0.2);
    }

    .onboarding-step-num {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 36px;
      height: 36px;
      border-radius: 10px;
      background: var(--bg-surface);
      border: 1px solid var(--border);
      color: var(--primary);
      font-weight: 800;
      font-size: 1.1rem;
    }

    .onboarding-card h3 {
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text-main);
    }

    .onboarding-card p {
      font-size: 0.9rem;
      color: var(--text-muted);
      line-height: 1.5;
    }

    .onboarding-code {
      background: #06070a;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 6px;
      padding: 10px 12px;
      font-family: Consolas, monospace;
      font-size: 0.82rem;
      color: #e2e8f0;
      line-height: 1.5;
    }

    .onboarding-optional-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
    }

    .optional-feature-card {
      background: rgba(19, 23, 34, 0.5);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 18px 20px;
      display: flex;
      gap: 14px;
      align-items: flex-start;
    }

    .optional-icon {
      font-size: 1.6rem;
      line-height: 1;
    }

    .optional-content h4 {
      font-size: 0.95rem;
      font-weight: 700;
      margin-bottom: 4px;
      color: var(--text-main);
    }

    .optional-content p {
      font-size: 0.84rem;
      color: var(--text-muted);
      line-height: 1.4;
      margin-bottom: 8px;
    }

    .optional-link {
      color: var(--accent);
      text-decoration: none;
      font-size: 0.84rem;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .optional-link:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>

  <!-- HEADER NETFLIX -->
  <header>
    <div class="header-content">
      <div class="header-left">
        <div class="brand" onclick="switchView('home')">
          <div class="brand-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect>
              <line x1="7" y1="2" x2="7" y2="22"></line>
              <line x1="17" y1="2" x2="17" y2="22"></line>
              <line x1="2" y1="12" x2="22" y2="12"></line>
              <line x1="2" y1="7" x2="7" y2="7"></line>
              <line x1="2" y1="17" x2="7" y2="17"></line>
              <line x1="17" y1="17" x2="22" y2="17"></line>
              <line x1="17" y1="7" x2="22" y2="7"></line>
            </svg>
          </div>
          <div>
            <div style="display: flex; align-items: center; gap: 6px;">
              <span class="brand-title">CineLocal</span>
              <span class="brand-badge">Stream</span>
            </div>
          </div>
        </div>

        <nav class="main-nav">
          <button id="navHome" class="nav-btn active" onclick="switchView('home')">
            Início
          </button>
          <button id="navMovies" class="nav-btn" onclick="switchView('movies')">
            Filmes
          </button>
          <button id="navSeries" class="nav-btn" onclick="switchView('series')">
            Séries
          </button>
        </nav>
      </div>

      <div class="header-right">
        <div class="search-container">
          <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input 
            type="text" 
            id="globalSearchInput" 
            class="search-input" 
            placeholder="Buscar títulos, atores, diretor... (atalho /)" 
            oninput="handleSearchInput(this.value)"
          >
          <button id="searchClearBtn" class="search-clear" onclick="clearSearch()">&times;</button>
        </div>

        <button class="btn-header-action" onclick="openSurpriseModal()" title="Sortear Filme Aleatório (Roleta)">
          <span style="font-size: 13px;">🎲</span> Surpreenda-me
        </button>

        <button class="btn-header-action" onclick="openQrConnectModal('remote')" title="Abrir Controle Remoto Virtual no Celular">
          <span style="font-size: 13px;">📱</span> Controle
        </button>

        <button class="btn-header-action" onclick="openQrConnectModal('tv')" title="Conectar Smart TV ou Celular">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="5" y="2" width="14" height="20" rx="2"></rect>
            <line x1="12" y1="18" x2="12.01" y2="18"></line>
          </svg>
          TV / Celular
        </button>

        <div id="protocolBadge" class="badge-protocol badge-local">
          <span id="protocolText">Modo Portátil</span>
        </div>

        <button class="btn-header-action" onclick="showHelpModal()" title="Instruções de Uso">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
            <line x1="12" y1="17" x2="12.01" y2="17"></line>
          </svg>
          Ajuda
        </button>
      </div>
    </div>
  </header>

  <!-- VIEW 1: HOME (HERO BANNER + CARROSÉIS NETFLIX) -->
  <main id="homeView">
    <!-- HERO BANNER DINÂMICO -->
    <section id="heroBanner" class="hero-banner">
      <div class="hero-backdrop-gradient"></div>
      <div class="hero-content">
        <span class="hero-badge-tag" id="heroTag">Destaque CineLocal</span>
        <h1 class="hero-title" id="heroTitle">Carregando...</h1>
        <div class="hero-meta">
          <span id="heroYear">2024</span>
          <span class="badge-res" id="heroRes">4K UHD</span>
          <span id="heroExtra">Áudio Original • Dublado</span>
        </div>
        <p class="hero-overview" id="heroDesc">
          Aproveite a sua biblioteca completa com qualidade cinema de transmissão local e som surround imersivo.
        </p>
        <div class="hero-buttons">
          <button class="btn-hero-play" id="heroBtnPlay" onclick="playHeroMedia()">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <polygon points="5 3 19 12 5 21 5 3"></polygon>
            </svg>
            Assistir Agora
          </button>
          <button class="btn-hero-vlc" id="heroBtnVlc" onclick="vlcHeroMedia()">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2L4 18h16L12 2zm0 4.5l4.5 9h-9L12 6.5zM7 20h10v2H7v-2z"/>
            </svg>
            Assistir no VLC
          </button>
        </div>
      </div>
    </section>

    <!-- TRILHOS / CARROSÉIS DA HOME -->
    <div id="homeCarouselsContainer">
      <!-- Injetado dinamicamente -->
    </div>
  </main>

  <!-- VIEW 2: FILMES (CATÁLOGO COMPLETO) -->
  <main id="moviesView" class="view-container" style="display: none;">
    <div class="view-header">
      <div class="view-title-group">
        <h2>Catálogo de Filmes</h2>
        <p id="moviesCountLabel">Carregando títulos...</p>
      </div>

      <div class="filter-chips">
        <button class="chip active" data-filter="all" onclick="setMovieFilter('all')">Todos</button>
        <button class="chip" data-filter="favorites" onclick="setMovieFilter('favorites')">⭐ Minha Lista</button>
        <button class="chip" data-filter="unwatched" onclick="setMovieFilter('unwatched')">Não Assistidos</button>
        <button class="chip" data-filter="franchise" onclick="setMovieFilter('franchise')">Franquias</button>
        <button class="chip" data-filter="standalone" onclick="setMovieFilter('standalone')">Filmes Avulsos</button>
        <button class="chip" data-filter="4k" onclick="setMovieFilter('4k')">4K UHD</button>
        <button class="chip" data-filter="1080p" onclick="setMovieFilter('1080p')">1080p</button>
        <select id="genreSelectFilter" onchange="setMovieGenreFilter(this.value)" class="filter-select" title="Filtrar por Gênero">
          <option value="">Gênero: Todos</option>
        </select>
        <select id="yearSelectFilter" onchange="setMovieYearFilter(this.value)" class="filter-select" title="Filtrar por Ano / Década">
          <option value="">Ano: Todos</option>
          <option value="2020">2020 em diante</option>
          <option value="2010">2010 - 2019</option>
          <option value="2000">Anos 2000</option>
          <option value="classic">Clássicos (Antes de 2000)</option>
        </select>
      </div>
    </div>

    <div id="moviesGrid" class="grid-layout">
      <!-- Grid de Filmes -->
    </div>
  </main>

  <!-- VIEW 3: SÉRIES (CATÁLOGO DEDICADO) -->
  <main id="seriesView" class="view-container" style="display: none;">
    <div class="view-header">
      <div class="view-title-group">
        <h2>Séries e Temporadas</h2>
        <p id="seriesCountLabel">Séries organizadas em episódios</p>
      </div>
    </div>

    <div id="seriesGrid" class="grid-layout">
      <!-- Grid de Séries -->
    </div>
  </main>

  <!-- MODAL DE SÉRIE ESTILO NETFLIX -->
  <div id="seriesModal" class="series-modal" onclick="closeSeriesModalOnOut(event)">
    <div class="series-modal-box">
      <button class="series-modal-close" onclick="closeSeriesModal()">&times;</button>
      
      <div class="series-modal-header">
        <img id="seriesModalPoster" class="series-modal-poster" src="" alt="Poster Série">
        <div class="series-modal-info" style="flex: 1;">
          <div class="series-modal-title" id="seriesModalTitle">Nome da Série</div>
          <div class="series-modal-meta" id="seriesModalMeta">
            <span id="seriesModalYear">2022</span> • 
            <span id="seriesModalSeasonsCount">1 Temporada</span> • 
            <span id="seriesModalEpisodesCount">8 Episódios</span>
            <span id="seriesModalRating" class="rating-badge">⭐ 8.5</span>
            <span id="seriesModalAudioBadge" class="badge-tag"></span>
            <span id="seriesModalSubBadge" class="badge-tag badge-sub" title="Legendas disponíveis">CC</span>
          </div>
          
          <div class="modal-genres-row" id="seriesModalGenres"></div>
          
          <p class="series-modal-desc" id="seriesModalDesc"></p>
          
          <div class="modal-credits">
            <div id="seriesModalCreator"></div>
            <div id="seriesModalCast"></div>
          </div>

          <div class="modal-links-row" id="seriesModalLinks"></div>
          <div style="margin-top: 14px; display: flex; gap: 8px; flex-wrap: wrap;">
            <button class="btn-watched-toggle" id="seriesModalBtnWatched" onclick="toggleWatchedCurrentSeries()">
              ✓ Já Assistido
            </button>
            <button class="btn-vlc-secondary" id="seriesModalBtnFavorite" onclick="toggleFavoriteCurrentSeries()">
              ⭐ Minha Lista
            </button>
            <button class="btn-vlc-secondary" id="seriesModalBtnTrailer" onclick="openTrailerCurrentSeries()">
              🎬 Trailer
            </button>
          </div>
        </div>
      </div>

      <div class="series-seasons-tabs" id="seriesSeasonsTabs">
        <!-- Abas de Temporada -->
      </div>

      <div class="series-episodes-list" id="seriesEpisodesList">
        <!-- Lista de Episódios -->
      </div>
    </div>
  </div>

  <!-- MODAL DE DETALHES DO FILME -->
  <div id="movieDetailsModal" class="series-modal" onclick="closeMovieModalOnOut(event)">
    <div class="series-modal-box">
      <button class="series-modal-close" onclick="closeMovieModal()">&times;</button>
      
      <div class="series-modal-header">
        <img id="movieModalPoster" class="series-modal-poster" src="" alt="Poster Filme">
        <div class="series-modal-info" style="flex: 1;">
          <div class="series-modal-title" id="movieModalTitle">Nome do Filme</div>
          <div class="series-modal-meta">
            <span id="movieModalYear">2020</span> • 
            <span id="movieModalRes">1080p</span> • 
            <span id="movieModalFormat">MKV</span> • 
            <span id="movieModalSize">2.5 GB</span>
            <span id="movieModalRating" class="rating-badge">⭐ 8.5</span>
            <span id="movieModalAudioBadge" class="badge-tag"></span>
            <span id="movieModalSubBadge" class="badge-tag badge-sub" title="Legendas disponíveis">CC</span>
          </div>
          
          <div class="modal-genres-row" id="movieModalGenres"></div>
          
          <p class="series-modal-desc" id="movieModalDesc">Sinopse do filme...</p>
          
          <div class="modal-credits">
            <div id="movieModalDirector"></div>
            <div id="movieModalCast"></div>
          </div>

          <div class="modal-links-row" id="movieModalLinks"></div>

          <div class="movie-modal-actions">
            <button class="btn-play-primary" id="movieModalBtnPlay" onclick="playMovieFromModal()">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <polygon points="5 3 19 12 5 21 5 3"></polygon>
              </svg>
              <span id="movieModalPlayText">Assistir no Navegador</span>
            </button>
            <button class="btn-vlc-secondary" id="movieModalBtnResume" onclick="resumeMovieFromModal()" style="display: none; background: rgba(229, 9, 20, 0.25); border-color: var(--primary); color: #fff;">
              ⏱️ Continuar de 00:00:00
            </button>
            <button class="btn-vlc-secondary" id="movieModalBtnFavorite" onclick="toggleFavoriteCurrentMovie()">
              ⭐ Minha Lista
            </button>
            <button class="btn-vlc-secondary" id="movieModalBtnTrailer" onclick="openTrailerCurrentMovie()">
              🎬 Trailer
            </button>
            <button class="btn-vlc-secondary" id="movieModalBtnVlc" onclick="vlcMovieFromModal()">
              Assistir no VLC (Áudio 5.1)
            </button>
            <button class="btn-watched-toggle" id="movieModalBtnWatched" onclick="toggleWatchedCurrentMovie()">
              ✓ Já Assistido
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- MODAL RASTREADOR & LINHA DO TEMPO DO MCU (66 TÍTULOS) -->
  <div id="mcuTrackerModal" class="series-modal" onclick="closeMcuTrackerOnOut(event)">
    <div class="series-modal-box mcu-modal-box">
      <button class="series-modal-close" onclick="closeMcuTrackerModal()">&times;</button>
      
      <div class="mcu-modal-header">
        <div class="mcu-header-brand-row">
          <span class="mcu-studios-tag">MARVEL STUDIOS</span>
          <span class="badge-tag" style="background: rgba(229,9,20,0.2); border: 1px solid #e50914; color: #ffb4b4;">LINHA DO TEMPO OFICIAL</span>
        </div>
        <h2 class="mcu-modal-title">⚡ Linha do Tempo Canônica & Rastreador do MCU</h2>
        <p class="mcu-modal-subtitle">Ordem cronológica completa da Saga do Infinito e Saga do Multiverso (da década de 1940 até os lançamentos de 2026)</p>
        
        <div class="mcu-stats-dashboard">
          <div class="mcu-stat-card">
            <div class="mcu-stat-card-val" id="mcuStatTotal">66</div>
            <div class="mcu-stat-card-lbl">Total Canônico</div>
          </div>
          <div class="mcu-stat-card">
            <div class="mcu-stat-card-val accent" id="mcuStatDownloaded">0</div>
            <div class="mcu-stat-card-lbl">Na Sua Coleção</div>
          </div>
          <div class="mcu-stat-card">
            <div class="mcu-stat-card-val" id="mcuStatMissing" style="color: #cbd5e1;">0</div>
            <div class="mcu-stat-card-lbl">Faltando Baixar</div>
          </div>
          <div class="mcu-stat-card">
            <div class="mcu-stat-card-val" id="mcuStatPercent" style="color: #f5c518;">0%</div>
            <div class="mcu-stat-card-lbl">Coleção Completa</div>
          </div>
        </div>
        
        <div class="mcu-progress-large">
          <div id="mcuProgressLargeFill" class="mcu-progress-large-fill" style="width: 0%;"></div>
        </div>
      </div>

      <div class="mcu-controls-bar">
        <div class="mcu-search-box">
          <span class="mcu-search-icon">🔍</span>
          <input type="text" id="mcuSearchInput" class="mcu-search-input" placeholder="Pesquisar filme ou série na cronologia..." oninput="filterMcuList()">
        </div>
        <div class="mcu-filter-chips">
          <button class="mcu-chip active" data-filter="all" onclick="setMcuFilter('all')">Todos (66)</button>
          <button class="mcu-chip" data-filter="downloaded" onclick="setMcuFilter('downloaded')">✓ Na Minha Coleção (<span id="mcuChipDownloadedCount">0</span>)</button>
          <button class="mcu-chip" data-filter="missing" onclick="setMcuFilter('missing')">⏳ Faltando Baixar (<span id="mcuChipMissingCount">0</span>)</button>
          <button class="mcu-chip" data-filter="movie" onclick="setMcuFilter('movie')">🎬 Filmes</button>
          <button class="mcu-chip" data-filter="series" onclick="setMcuFilter('series')">📺 Séries</button>
        </div>
      </div>

      <div class="mcu-timeline-body" id="mcuTimelineList">
        <!-- Lista interativa gerada dinamicamente via JS -->
      </div>
    </div>
  </div>

  <!-- CINEMA PLAYER -->
  <div id="playerModal" class="player-modal">
    <div id="playerContainer" class="player-container">
      
      <div class="player-top-bar">
        <button class="player-back-btn" onclick="closePlayer()">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          Voltar
        </button>

        <div class="player-movie-heading">
          <div id="playerTitle" class="player-movie-title">Título</div>
          <div id="playerSubInfo" class="player-movie-sub">Metadados</div>
        </div>

        <button class="player-back-btn" onclick="closePlayer()" title="Fechar">
          &times;
        </button>
      </div>

      <div class="video-viewport" id="videoViewport" onclick="handleViewportClick(event)">
        <video id="mainVideo" playsinline></video>

        <div id="subtitleDisplay" class="subtitle-display size-md">
          <span id="subtitleText" class="subtitle-text" style="display: none;"></span>
        </div>

        <div id="playerCenterFeedback" class="player-center-feedback" style="display: none;">
          <div class="feedback-bubble">
            <svg id="fbIconPlay" width="38" height="38" viewBox="0 0 24 24" fill="currentColor">
              <polygon points="5 3 19 12 5 21 5 3"></polygon>
            </svg>
            <svg id="fbIconPause" width="38" height="38" viewBox="0 0 24 24" fill="currentColor" style="display: none;">
              <rect x="6" y="4" width="4" height="16"></rect>
              <rect x="14" y="4" width="4" height="16"></rect>
            </svg>
          </div>
        </div>

        <div id="nextEpisodeToast" class="next-episode-toast" style="display: none;">
          <div class="next-ep-content">
            <div class="next-ep-badge">Próximo Episódio em <strong id="nextEpCountdown">15</strong>s</div>
            <div class="next-ep-name" id="nextEpTitle">Próximo Episódio</div>
          </div>
          <button class="btn-next-play" onclick="playNextEpisodeImmediately()">Assistir ⏭</button>
          <button class="btn-next-cancel" onclick="dismissNextEpisodeCountdown()" title="Cancelar">&times;</button>
        </div>
      </div>

      <div class="player-bottom-controls" onclick="event.stopPropagation()">
        <div class="seek-bar-container" id="seekBarContainer" onclick="handleSeekClick(event)">
          <div class="seek-bar-track">
            <div id="seekBuffered" class="seek-bar-buffered"></div>
            <div id="seekFill" class="seek-bar-fill"></div>
          </div>
        </div>

        <div class="controls-row">
          <div class="controls-left">
            <button class="btn-ctrl" onclick="togglePlayPause()" title="Play / Pause (Espaço)">
              <svg id="playIcon" width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
                <polygon points="5 3 19 12 5 21 5 3"></polygon>
              </svg>
              <svg id="pauseIcon" width="22" height="22" viewBox="0 0 24 24" fill="currentColor" style="display: none;">
                <rect x="6" y="4" width="4" height="16"></rect>
                <rect x="14" y="4" width="4" height="16"></rect>
              </svg>
            </button>

            <button class="btn-ctrl" onclick="skipTime(-10)" title="Voltar 10s (←)">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 4v6h6M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/>
              </svg>
            </button>

            <button class="btn-ctrl" onclick="skipTime(10)" title="Avançar 10s (→)">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M23 4v6h-6M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
              </svg>
            </button>

            <button id="btnNextEpisode" class="btn-ctrl" onclick="playNextEpisode()" title="Próximo Episódio (N)" style="display: none;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <polygon points="5 4 15 12 5 20 5 4"></polygon>
                <line x1="19" y1="5" x2="19" y2="19" stroke="currentColor" stroke-width="2.5"></line>
              </svg>
            </button>

            <!-- CONTROLE DE VOLUME & SUPER BOOSTER -->
            <div class="volume-container">
              <button class="btn-ctrl" id="btnMute" onclick="toggleMute()" title="Mudo / Desmutar (M)">
                <svg id="volIconHigh" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                  <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                </svg>
                <svg id="volIconLow" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display: none;">
                  <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                  <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                </svg>
                <svg id="volIconMuted" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display: none; color: #ef4444;">
                  <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                  <line x1="23" y1="9" x2="17" y2="15"></line>
                  <line x1="17" y1="9" x2="23" y2="15"></line>
                </svg>
              </button>
              <div class="volume-slider-box">
                <input type="range" id="volumeSlider" min="0" max="300" step="1" value="100" class="volume-slider" oninput="setPlayerVolume(this.value)" title="Volume (0% - 300%)">
                <span id="volumePercent" class="volume-percent" onclick="cycleVolumeBoost()" title="Clique para alternar Boost (100% / 150% / 200% / 300%)">100%</span>
              </div>
            </div>

            <span id="timeDisplay" class="time-display">00:00:00 / 00:00:00</span>
          </div>

          <div class="controls-right">
            <!-- VLC -->
            <button class="btn-ctrl" onclick="launchCurrentInVlc()" title="Abrir no VLC Portable (V)">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="#ff8800">
                <path d="M12 2L4 18h16L12 2zm0 4.5l4.5 9h-9L12 6.5zM7 20h10v2H7v-2z"/>
              </svg>
            </button>

            <!-- VELOCIDADE DE REPRODUÇÃO -->
            <button class="btn-ctrl" id="btnSpeed" onclick="cyclePlaybackSpeed()" title="Velocidade de Reprodução ([ / ])">
              <span id="speedLabel" style="font-size: 12px; font-weight: 800; min-width: 22px;">1x</span>
            </button>

            <!-- PICTURE IN PICTURE -->
            <button class="btn-ctrl" id="btnPiP" onclick="togglePictureInPicture()" title="Janela Flutuante / PiP (P)">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="3" width="20" height="14" rx="2"></rect>
                <rect x="12" y="9" width="8" height="6" rx="1" fill="currentColor"></rect>
              </svg>
            </button>

            <!-- AUDIO TRACKS MENU -->
            <div class="dropdown">
              <button class="btn-ctrl" onclick="toggleDropdown('audioMenu')" title="Faixas de Áudio">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3 18v-6a9 9 0 0 1 18 0v6"></path>
                  <path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"></path>
                </svg>
              </button>
              <div id="audioMenu" class="dropdown-menu" style="min-width: 240px;">
                <div style="font-size: 11px; font-weight: 800; color: var(--primary); text-transform: uppercase; padding: 4px 8px;">Faixa de Áudio</div>
                <div id="audioTracksList"></div>
              </div>
            </div>

            <!-- SUBTITLES MENU -->
            <div class="dropdown">
              <button class="btn-ctrl" onclick="toggleDropdown('subtitlesMenu')" title="Legendas (C)">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                </svg>
              </button>
              <div id="subtitlesMenu" class="dropdown-menu" style="min-width: 250px;">
                <div style="font-size: 11px; font-weight: 800; color: var(--primary); text-transform: uppercase; padding: 4px 8px;">Legendas</div>
                <div id="subtitlesList"></div>
                <hr style="border: 0; border-top: 1px solid var(--border); margin: 6px 0;">
                <div style="font-size: 11px; font-weight: 700; color: var(--text-muted); padding: 4px 8px;">Tamanho</div>
                <div style="display: flex; gap: 4px; padding: 4px 8px;">
                  <button class="season-tab" onclick="setSubSize('sm')">P</button>
                  <button class="season-tab active" onclick="setSubSize('md')">M</button>
                  <button class="season-tab" onclick="setSubSize('lg')">G</button>
                  <button class="season-tab" onclick="setSubSize('xl')">GG</button>
                </div>
                <hr style="border: 0; border-top: 1px solid var(--border); margin: 6px 0;">
                <div style="font-size: 11px; font-weight: 700; color: var(--text-muted); padding: 4px 8px; display: flex; justify-content: space-between; align-items: center;">
                  <span>Sincronia / Delay</span>
                  <span id="subSyncValueLabel" style="color: #ff9922; font-weight: 800;">0.0s</span>
                </div>
                <div style="display: flex; gap: 4px; padding: 4px 8px; align-items: center; justify-content: space-between;">
                  <button class="season-tab" onclick="adjustSubSync(-0.5)" title="Atrasar legenda em 0.5s">-0.5s</button>
                  <button class="season-tab" onclick="adjustSubSync(-0.1)" title="Atrasar legenda em 0.1s">-0.1s</button>
                  <button class="season-tab" onclick="resetSubSync()" title="Redefinir sincronia">0s</button>
                  <button class="season-tab" onclick="adjustSubSync(0.1)" title="Adiantar legenda em 0.1s">+0.1s</button>
                  <button class="season-tab" onclick="adjustSubSync(0.5)" title="Adiantar legenda em 0.5s">+0.5s</button>
                </div>
                <div style="font-size: 10px; color: var(--text-muted); padding: 2px 8px 4px; line-height: 1.3;">
                  Use <strong>-</strong> para atrasar ou <strong>+</strong> para adiantar se notar delay na TV.
                </div>
              </div>
            </div>

            <!-- FULLSCREEN -->
            <button class="btn-ctrl" onclick="toggleFullscreen()" title="Tela Cheia (F)">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- MODAL SURPREENDA-ME (ROLETA DE FILMES) -->
  <div id="surpriseModal" class="series-modal" onclick="closeSurpriseModalOnOut(event)">
    <div class="series-modal-box" style="max-width: 580px; padding: 28px; text-align: center;">
      <button class="series-modal-close" onclick="closeSurpriseModal()">&times;</button>
      <div style="font-size: 2.8rem; margin-bottom: 8px;">🎲</div>
      <h2 style="font-size: 1.4rem; color: #fff; margin-bottom: 4px;">O que assistir hoje?</h2>
      <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 20px;">O CineLocal sorteou um filme especial para você:</p>
      
      <div id="surpriseCardBox" class="surprise-card-box">
        <img id="surprisePoster" class="surprise-poster" src="" alt="Poster">
        <div style="flex: 1;">
          <h3 id="surpriseTitle" style="font-size: 1.15rem; font-weight: 800; color: #fff; margin-bottom: 6px;">Título</h3>
          <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 8px;">
            <span id="surpriseYear">2020</span> • <span id="surpriseRes">1080p</span> • <span id="surpriseRating" class="rating-badge">⭐ 8.0</span>
          </div>
          <p id="surpriseOverview" style="font-size: 12px; color: #cbd5e1; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; margin: 0;"></p>
        </div>
      </div>
      
      <div style="display: flex; gap: 12px; justify-content: center; margin-top: 22px;">
        <button class="btn-play-primary" id="btnSurprisePlay">
          ▶ Assistir Agora
        </button>
        <button class="btn-vlc-secondary" onclick="spinSurpriseMovie()">
          🎲 Sortear Outro
        </button>
      </div>
    </div>
  </div>

  <!-- MODAL DE TRAILER OFICIAL -->
  <div id="trailerModal" class="series-modal" onclick="closeTrailerModalOnOut(event)">
    <div class="series-modal-box" style="max-width: 860px; padding: 0; overflow: hidden; background: #0b0e14;">
      <div style="display: flex; justify-content: space-between; align-items: center; padding: 14px 20px; border-bottom: 1px solid var(--border);">
        <div style="font-weight: 800; font-size: 1.1rem; color: #fff; display: flex; align-items: center; gap: 8px;">
          <span>🎬 Trailer Oficial:</span>
          <span id="trailerModalTitle" style="color: var(--primary);"></span>
        </div>
        <button class="series-modal-close" style="position: static;" onclick="closeTrailerModal()">&times;</button>
      </div>
      <div style="position: relative; width: 100%; padding-bottom: 56.25%; height: 0; background: #000;">
        <iframe id="trailerIframe" style="position: absolute; top:0; left: 0; width: 100%; height: 100%; border: none;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
      </div>
    </div>
  </div>

  <!-- MODAL CONECTAR TV / CONTROLE REMOTO (QR CODE) -->
  <div id="qrModal" class="series-modal" onclick="closeQrModalOnOut(event)">
    <div class="series-modal-box qr-modal-box">
      <button class="series-modal-close" onclick="closeQrModal()">&times;</button>
      
      <div class="qr-tab-bar">
        <button id="qrTabTv" class="qr-tab-btn active" onclick="switchQrTab('tv')">📺 Assistir na TV</button>
        <button id="qrTabRemote" class="qr-tab-btn" onclick="switchQrTab('remote')">📱 Controle no Celular</button>
      </div>

      <h2 id="qrModalTitle" style="font-size: 1.3rem; color: #fff; margin-bottom: 6px;">Conectar Smart TV ou Celular</h2>
      <p id="qrModalDesc" style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 16px;">
        Conecte seu dispositivo na mesma rede Wi-Fi e aponte a câmera para abrir o CineLocal:
      </p>

      <div class="qr-container-box">
        <div id="qrSvgWrapper"></div>
      </div>

      <div class="onboarding-code" id="qrLocalUrlDisplay" style="font-size: 1.1rem; font-weight: 800; color: #00ff88; margin: 12px 0;">
        http://localhost:8000/
      </div>

      <p style="color: var(--text-muted); font-size: 0.8rem; margin: 0;">
        Disponível na sua rede local sem necessidade de instalação.
      </p>
    </div>
  </div>

  <!-- TOASTS -->
  <div id="toastContainer" class="toast-container"></div>

  <!-- CARREGA OS METADADOS -->
  <script src="catalogo.js" onerror="console.log('catalogo.js ausente ou inicial.');"></script>

  <!-- JAVASCRIPT DO SISTEMA -->
  <script>
    // Garantir que variaveis globais existam mesmo antes do catalogo.js ser gerado
    window.CATALOGO = window.CATALOGO || [];
    window.CATALOGO_FILMES = window.CATALOGO_FILMES || [];
    window.CATALOGO_SERIES = window.CATALOGO_SERIES || [];
    window.LEGENDAS_DB = window.LEGENDAS_DB || {};

    const state = {
      all: [],
      catalogo: [],
      movies: [],
      series: [],
      activeView: 'home',
      movieFilter: 'all',
      genreFilter: '',
      yearFilter: '',
      searchQuery: '',
      heroMedia: null,
      currentPlaying: null, // movie ou episode
      currentEpisodeSeries: null,
      currentSeasonIndex: 0,
      activeSubtitle: null,
      subtitleCues: [],
      subSyncOffset: parseFloat(localStorage.getItem('cinelocal_sub_sync_offset')) || 0.0,
      subSize: 'md',
      playbackSpeed: 1.0,
      controlsTimeout: null,
      vlcAvailable: true,
      ffmpegAvailable: true,
      localIp: 'localhost',
      localUrl: 'http://localhost:8000/',
      nextEpCountdownActive: false,
      nextEpDismissed: false,
      currentSurpriseMovie: null,
      favorites: JSON.parse(localStorage.getItem('cinelocal_favorites') || '[]'),
      audioTracks: [],
      watchProgress: JSON.parse(localStorage.getItem('cinelocal_watch_progress') || '{}'),
      watchedList: JSON.parse(localStorage.getItem('cinelocal_watched_list') || '{}')
    };

    document.addEventListener('DOMContentLoaded', async () => {
      detectProtocol();
      setupKeyboardShortcuts();
      setupSeekDrag();
      setupPlayerEvents();

      // Se rodando via HTTP, consulta capacidades de VLC, FFmpeg e IP LAN
      if (window.location.protocol.startsWith('http')) {
        try {
          const capRes = await fetch('/api/capabilities');
          if (capRes.ok) {
            const caps = await capRes.json();
            state.vlcAvailable = caps.vlcAvailable;
            state.ffmpegAvailable = caps.ffmpegAvailable;
            if (caps.localIp) state.localIp = caps.localIp;
            if (caps.localUrl) {
              state.localUrl = caps.localUrl;
              const qrDisplay = document.getElementById('qrLocalUrlDisplay');
              if (qrDisplay) qrDisplay.innerText = caps.localUrl;
            }
          }
        } catch (e) {}

        // Sincroniza progresso de reprodução e favoritos globais com o servidor
        try {
          const userRes = await fetch('/api/user_state');
          if (userRes.ok) {
            const userData = await userRes.json();
            if (userData.watchProgress) {
              state.watchProgress = Object.assign({}, state.watchProgress, userData.watchProgress);
              localStorage.setItem('cinelocal_watch_progress', JSON.stringify(state.watchProgress));
            }
            if (userData.favorites) {
              state.favorites = Array.from(new Set([...state.favorites, ...userData.favorites]));
              localStorage.setItem('cinelocal_favorites', JSON.stringify(state.favorites));
            }
          }
        } catch (e) {}

        // Inicia ouvinte de comandos do controle remoto virtual (Celular -> TV)
        setupRemoteControlListener();
      }

      // Carregar catálogo
      if (window.CATALOGO) {
        state.all = window.CATALOGO;
        state.catalogo = window.CATALOGO;
      }
      if (window.CATALOGO_FILMES) {
        state.movies = window.CATALOGO_FILMES;
      } else {
        state.movies = state.all.filter(x => x.type === 'movie');
      }
      if (window.CATALOGO_SERIES) {
        state.series = window.CATALOGO_SERIES;
      } else {
        state.series = state.all.filter(x => x.type === 'series');
      }

      // Se rodando via HTTP, tenta puxar dinamicamente caso queira sincronizar
      if (window.location.protocol.startsWith('http')) {
        try {
          const res = await fetch('/api/filmes');
          if (res.ok) {
            const data = await res.json();
            if (data.catalog) {
              state.all = data.catalog;
              state.catalogo = data.catalog;
              state.movies = data.movies || data.catalog.filter(x => x.type === 'movie');
              state.series = data.series || data.catalog.filter(x => x.type === 'series');
            }
          }
        } catch (e) {}
      }

      setupHeroBanner();
      renderHomeCarousels();
      populateGenreFilter();
      renderMoviesGrid();
      renderSeriesGrid();
      updateSubSyncUI();
    });

    function detectProtocol() {
      const isHttp = window.location.protocol.startsWith('http');
      const badge = document.getElementById('protocolBadge');
      const text = document.getElementById('protocolText');
      if (isHttp) {
        badge.className = 'badge-protocol badge-lan';
        text.innerText = 'Servidor LAN Ativo';
      } else {
        badge.className = 'badge-protocol badge-local';
        text.innerText = 'Modo Portátil';
      }
    }

    /* CONTROLE DE VIEWS (Início, Filmes, Séries) */
    function switchView(viewName) {
      state.activeView = viewName;
      document.getElementById('navHome').classList.toggle('active', viewName === 'home');
      document.getElementById('navMovies').classList.toggle('active', viewName === 'movies');
      document.getElementById('navSeries').classList.toggle('active', viewName === 'series');

      document.getElementById('homeView').style.display = viewName === 'home' ? 'block' : 'none';
      document.getElementById('moviesView').style.display = viewName === 'movies' ? 'block' : 'none';
      document.getElementById('seriesView').style.display = viewName === 'series' ? 'block' : 'none';

      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    /* HERO BANNER DINÂMICO */
    function setupHeroBanner() {
      const hero = document.getElementById('heroBanner');
      // Prioridade para destaque épico
      const candidates = state.movies.filter(m => 
        (m.resolution && m.resolution.includes('4K')) || 
        ['Interestelar', 'Batman', 'Vingadores', 'Gladiador', 'A Origem'].some(t => m.title.includes(t))
      );
      const chosen = candidates.length > 0 ? candidates[Math.floor(Math.random() * candidates.length)] : (state.movies[0] || state.series[0]);
      if (!chosen) {
        if (hero) hero.style.display = 'none';
        return;
      }

      if (hero) hero.style.display = 'block';
      const heroVlc = document.getElementById('heroBtnVlc');
      if (heroVlc) heroVlc.style.display = state.vlcAvailable ? 'inline-flex' : 'none';

      state.heroMedia = chosen;
      hero.style.backgroundImage = `url('${encodeURI(chosen.posterPath)}')`;

      document.getElementById('heroTitle').innerText = chosen.title;
      document.getElementById('heroYear').innerText = chosen.year || '2024';
      document.getElementById('heroRes').innerText = chosen.resolution || '1080p';
      document.getElementById('heroTag').innerText = chosen.franchise ? chosen.franchise : 'Destaque CineLocal';
      
      const descMap = {
        'A Origem': 'Dom Cobb é um ladrão habilidoso cuja arte é a espionagem corporativa através do mundo dos sonhos subconscientes.',
        'Gladiador': 'Um ex-general romano jura se vingar do imperador corrupto que assassinou sua família e o sentenciou à escravidão.',
        'Vingadores': 'Os heróis mais poderosos da Terra devem se unir e aprender a lutar como uma equipe para salvar a Terra.',
        'The Bear': 'Um jovem e brilhante chef assume o restaurante de sanduíches da família em Chicago, enfrentando caos e superação.',
        'Batman': 'Em Gotham City, o Cavaleiro das Trevas enfrenta os maiores criminosos do submundo para restaurar a ordem.'
      };
      
      let matchedDesc = 'Disponível em alta resolução com áudio multicanal imersivo e streaming ultra rápido via CineLocal.';
      for (const [k, d] of Object.entries(descMap)) {
        if (chosen.title.includes(k)) {
          matchedDesc = d;
          break;
        }
      }
      document.getElementById('heroDesc').innerText = matchedDesc;
    }

    function playHeroMedia() {
      if (state.heroMedia) {
        if (state.heroMedia.type === 'series') {
          openSeriesModal(state.heroMedia.id);
        } else {
          openPlayer(state.heroMedia);
        }
      }
    }

    function vlcHeroMedia() {
      if (state.heroMedia) {
        launchVlc(state.heroMedia.videoPath);
      }
    }

    /* GESTÃO DE PROGRESSO E ITENS ASSISTIDOS */
    function getWatchProgress(id) {
      return state.watchProgress[id] || null;
    }

    function saveWatchProgress(id, currentTime, duration, media) {
      if (!id || !duration || duration <= 0) return;
      const pct = Math.round((currentTime / duration) * 100);
      const completed = pct >= 92;

      state.watchProgress[id] = {
        id: id,
        currentTime: Math.floor(currentTime),
        duration: Math.floor(duration),
        pct: pct,
        completed: completed,
        timestamp: Date.now(),
        title: media.title || '',
        posterPath: media.posterPath || '',
        type: media.type || 'movie',
        resolution: media.resolution || '1080p',
        seriesId: state.currentEpisodeSeries ? state.currentEpisodeSeries.series.id : null,
        seriesTitle: state.currentEpisodeSeries ? state.currentEpisodeSeries.series.title : null,
        seasonIdx: state.currentEpisodeSeries ? state.currentEpisodeSeries.seasonIdx : null,
        epNum: state.currentEpisodeSeries ? state.currentEpisodeSeries.epNum : null
      };

      if (completed) {
        state.watchedList[id] = true;
        localStorage.setItem('cinelocal_watched_list', JSON.stringify(state.watchedList));
      }

      localStorage.setItem('cinelocal_watch_progress', JSON.stringify(state.watchProgress));

      // Sincroniza com o servidor local para manter Smart TV, Celular e PC alinhados
      if (window.location.protocol.startsWith('http')) {
        fetch('/api/progress', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            id: id,
            currentTime: currentTime,
            duration: duration,
            item: {
              title: media.title || '',
              posterPath: media.posterPath || '',
              isEpisode: !!state.currentEpisodeSeries,
              seriesId: state.currentEpisodeSeries ? state.currentEpisodeSeries.series.id : null,
              seasonIdx: state.currentEpisodeSeries ? state.currentEpisodeSeries.seasonIdx : null,
              episodeNumber: state.currentEpisodeSeries ? state.currentEpisodeSeries.epNum : null
            }
          }),
          keepalive: true
        }).catch(() => {});
      }
    }

    function isItemWatched(id) {
      if (state.watchedList[id]) return true;
      const p = state.watchProgress[id];
      return !!(p && p.completed);
    }

    function toggleWatched(id) {
      if (!id) return;
      state.watchedList[id] = !state.watchedList[id];
      localStorage.setItem('cinelocal_watched_list', JSON.stringify(state.watchedList));

      if (state.watchedList[id]) {
        if (state.watchProgress[id]) {
          state.watchProgress[id].completed = true;
          localStorage.setItem('cinelocal_watch_progress', JSON.stringify(state.watchProgress));
        }
        showToast('Marcado como assistido ✓');
      } else {
        if (state.watchProgress[id]) {
          state.watchProgress[id].completed = false;
          localStorage.setItem('cinelocal_watch_progress', JSON.stringify(state.watchProgress));
        }
        showToast('Desmarcado de assistidos');
      }

      renderHomeCarousels();
      renderMoviesGrid();
      renderSeriesGrid();
    }

    function clearProgressItem(id) {
      if (state.watchProgress[id]) {
        delete state.watchProgress[id];
        localStorage.setItem('cinelocal_watch_progress', JSON.stringify(state.watchProgress));
        renderHomeCarousels();
        renderMoviesGrid();
        showToast('Item removido de Continuar Assistindo');
      }
    }

    /* MINHA LISTA (FAVORITOS) */
    function isItemFavorite(id) {
      return state.favorites && state.favorites.includes(id);
    }

    function toggleFavorite(id) {
      if (!id) return;
      if (!state.favorites) state.favorites = [];
      const idx = state.favorites.indexOf(id);
      let isFav = false;
      if (idx !== -1) {
        state.favorites.splice(idx, 1);
        isFav = false;
        showToast('Removido da Minha Lista');
      } else {
        state.favorites.unshift(id);
        isFav = true;
        showToast('Adicionado à Minha Lista ⭐');
      }

      localStorage.setItem('cinelocal_favorites', JSON.stringify(state.favorites));

      if (window.location.protocol.startsWith('http')) {
        fetch('/api/favorite/toggle', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ id: id })
        }).catch(() => {});
      }

      renderHomeCarousels();
      renderMoviesGrid();
      renderSeriesGrid();
    }

    function toggleFavoriteCurrentMovie() {
      if (currentModalMovie) {
        toggleFavorite(currentModalMovie.id);
        const favBtn = document.getElementById('movieModalBtnFavorite');
        if (favBtn) {
          const isFav = isItemFavorite(currentModalMovie.id);
          favBtn.classList.toggle('active', isFav);
          favBtn.innerText = isFav ? '⭐ Na Minha Lista' : '⭐ Minha Lista';
        }
      }
    }

    function toggleFavoriteCurrentSeries() {
      const title = document.getElementById('seriesModalTitle').innerText;
      const series = state.series.find(s => s.title === title || s.id === title);
      if (series) {
        toggleFavorite(series.id);
        const favBtn = document.getElementById('seriesModalBtnFavorite');
        if (favBtn) {
          const isFav = isItemFavorite(series.id);
          favBtn.classList.toggle('active', isFav);
          favBtn.innerText = isFav ? '⭐ Na Minha Lista' : '⭐ Minha Lista';
        }
      }
    }

    /* MODAL DE TRAILER OFICIAL */
    function openTrailerModal(title, year) {
      const modal = document.getElementById('trailerModal');
      const titleEl = document.getElementById('trailerModalTitle');
      const iframe = document.getElementById('trailerIframe');
      if (!modal || !iframe) return;

      if (titleEl) titleEl.innerText = title;
      const q = encodeURIComponent(`trailer dublado oficial ${title} ${year || ''}`);
      iframe.src = `https://www.youtube-nocookie.com/embed?listType=search&list=${q}&autoplay=1`;
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
    }

    function closeTrailerModal() {
      const modal = document.getElementById('trailerModal');
      const iframe = document.getElementById('trailerIframe');
      if (modal) modal.classList.remove('active');
      if (iframe) iframe.src = '';
      document.body.style.overflow = '';
    }

    function closeTrailerModalOnOut(e) {
      if (e.target.id === 'trailerModal') closeTrailerModal();
    }

    function openTrailerCurrentMovie() {
      if (currentModalMovie) {
        openTrailerModal(currentModalMovie.title, currentModalMovie.year);
      }
    }

    function openTrailerCurrentSeries() {
      const title = document.getElementById('seriesModalTitle').innerText;
      const series = state.series.find(s => s.title === title || s.id === title);
      if (series) {
        openTrailerModal(series.title, series.year);
      }
    }

    /* RENDERIZAÇÃO DOS CARROSÉIS DA HOME (ESTILO NETFLIX) */
    function renderHomeCarousels() {
      const container = document.getElementById('homeCarouselsContainer');
      container.innerHTML = '';

      const totalItems = (state.all && state.all.length) || (state.movies.length + state.series.length);
      if (totalItems === 0) {
        renderOnboarding(container);
        return;
      }

      // 0. CONTINUAR ASSISTINDO (Em andamento: 2% a 91%)
      const continueItems = Object.values(state.watchProgress)
        .filter(p => p.pct >= 2 && p.pct < 92 && !p.completed)
        .sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0))
        .map(p => {
          if (p.type === 'episode' && p.seriesId) {
            const s = state.series.find(x => x.id === p.seriesId);
            if (s && s.seasons && s.seasons[p.seasonIdx]) {
              const ep = s.seasons[p.seasonIdx].episodes.find(e => e.episodeNumber === p.epNum);
              if (ep) {
                return {
                  ...ep,
                  id: p.id,
                  title: `${s.title}: E${String(p.epNum).padStart(2,'0')}`,
                  posterPath: s.posterPath,
                  type: 'episode',
                  seriesId: p.seriesId,
                  seasonIdx: p.seasonIdx,
                  epNum: p.epNum,
                  savedTime: p.currentTime
                };
              }
            }
          }
          const m = state.movies.find(x => x.id === p.id) || state.series.find(x => x.id === p.id);
          return m ? { ...m, savedTime: p.currentTime } : null;
        })
        .filter(Boolean);

      if (continueItems.length > 0) {
        addContinueWatchingCarousel(container, '⏱️ Continuar Assistindo', continueItems);
      }

      // 0.1 MINHA LISTA (FAVORITOS)
      if (state.favorites && state.favorites.length > 0) {
        const favItems = state.favorites
          .map(favId => state.movies.find(m => m.id === favId) || state.series.find(s => s.id === favId))
          .filter(Boolean);
        if (favItems.length > 0) {
          addCarousel(container, '⭐ Minha Lista', favItems);
        }
      }

      // 1. ADICIONADOS RECENTEMENTE (Ordenados pelo timestamp real mtime gravado no catalogo!)
      const recent = [...state.movies]
        .sort((a, b) => (b.addedAt || 0) - (a.addedAt || 0))
        .slice(0, 14);
      addCarousel(container, '🔥 Adicionados Recentemente', recent);

      // 2. SÉRIES (The Bear, Loki, etc.)
      if (state.series.length > 0) {
        addCarousel(container, '📺 Séries & Temporadas', state.series);
      }

      // 3. UNIVERSO MARVEL (ORDEM CRONOLÓGICA DO MCU)
      const allItems = state.all || state.catalogo || window.CATALOGO || [];
      const marvelItems = allItems
        .filter(m => m.franchise && m.franchise.toLowerCase().includes('marvel'))
        .sort((a, b) => (a.sequence || 99) - (b.sequence || 99));
      if (marvelItems.length > 0) {
        addMarvelCarousel(container, '⚡ Universo Marvel (Ordem Cronológica do MCU)', marvelItems);
      }

      // 4. GRANDES FRANQUIAS
      const sagas = state.movies.filter(m => m.franchise && !m.franchise.toLowerCase().includes('marvel'));
      if (sagas.length > 0) {
        addCarousel(container, '🏆 Franquias & Sagas Épicas', sagas);
      }

      // 5. TODOS OS FILMES
      addCarousel(container, '🎬 Catálogo Completo de Longas-Metragens', state.movies);
    }

    function addContinueWatchingCarousel(container, title, items) {
      if (!items || items.length === 0) return;

      const sectionId = 'carousel_continue';
      const section = document.createElement('section');
      section.className = 'carousel-section';

      section.innerHTML = `
        <div class="carousel-header">
          <div class="carousel-title-box">
            <h3 class="carousel-title">${title}</h3>
            <span class="carousel-count">${items.length} em andamento</span>
          </div>
        </div>
        <div class="carousel-track-wrapper">
          <button class="carousel-btn left" onclick="scrollTrack('${sectionId}', -600)">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
          </button>
          <div id="${sectionId}" class="carousel-track">
            ${items.map(item => {
              const prog = getWatchProgress(item.id);
              const pct = prog ? prog.pct : 0;
              const remSec = prog ? Math.max(0, prog.duration - prog.currentTime) : 0;
              const remMin = Math.round(remSec / 60);
              const clickAction = item.type === 'episode' 
                ? `playEpisode('${item.seriesId}', ${item.seasonIdx}, ${item.epNum}, ${prog ? prog.currentTime : 0})`
                : `openPlayerById('${item.id}', ${prog ? prog.currentTime : 0})`;

              return `
                <div class="movie-card dpad-focusable" tabindex="0" onclick="${clickAction}">
                  <div class="card-poster-wrapper">
                    <img class="card-poster" src="${encodeURI(item.posterPath || '')}" alt="${item.title}" loading="lazy">
                    <span class="card-badge badge-1080p">RESTAM ${remMin} MIN</span>
                    <div class="card-progress-bar">
                      <div class="card-progress-fill" style="width: ${pct}%"></div>
                    </div>
                  </div>
                  <div class="card-content">
                    <div>
                      <div class="card-title">${item.title}</div>
                      <div class="card-subinfo">Parou em ${formatTime(prog ? prog.currentTime : 0)} (${pct}%)</div>
                    </div>
                    <div class="card-actions">
                      <button class="card-btn-play" onclick="event.stopPropagation(); ${clickAction}">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                          <polygon points="5 3 19 12 5 21 5 3"></polygon>
                        </svg>
                        Retomar
                      </button>
                      <button class="card-btn-info" onclick="event.stopPropagation(); clearProgressItem('${item.id}')" title="Remover de Continuar Assistindo">
                        &times;
                      </button>
                    </div>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
          <button class="carousel-btn right" onclick="scrollTrack('${sectionId}', 600)">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </button>
        </div>
      `;

      container.appendChild(section);
    }

    function renderOnboarding(container) {
      container.innerHTML = `
        <div class="onboarding-container">
          <div class="onboarding-hero">
            <span class="onboarding-badge">🚀 Guia Inicial</span>
            <h1 class="onboarding-title">Bem-vindo ao CineLocal!</h1>
            <p class="onboarding-subtitle">
              Sua central particular de streaming doméstico de alta performance está pronta. 
              Siga os 3 passos simples abaixo para adicionar seus filmes ou séries:
            </p>
          </div>

          <div class="onboarding-steps">
            <div class="onboarding-card">
              <div class="onboarding-step-num">1</div>
              <h3>Coloque suas Mídias</h3>
              <p>Adicione qualquer arquivo de vídeo (MP4, MKV, AVI, WebM) e legendas .srt nas pastas de mídia do projeto:</p>
              <div class="onboarding-code">media/filmes/Nome do Filme (Ano)/<br>media/series/Nome da Serie/Season 01/</div>
            </div>

            <div class="onboarding-card">
              <div class="onboarding-step-num">2</div>
              <h3>Atualize o Catálogo</h3>
              <p>Dê dois cliques no atalho na raiz para escanear a pasta, indexar resoluções, áudio, sinopses e capas:</p>
              <div class="onboarding-code">Duplo clique em: Atualizar Catalogo.bat<br>ou execute: python app/atualizar_catalogo.py</div>
            </div>

            <div class="onboarding-card">
              <div class="onboarding-step-num">3</div>
              <h3>Dê o Play e Relaxe!</h3>
              <p>Recarregue a página no seu navegador para assistir com amplificador de volume de até 200% ou acesse da sua Smart TV.</p>
              <div class="onboarding-code">Smart TV / Celular: Iniciar Servidor (TV e Celular).bat</div>
            </div>
          </div>

          <h3 style="font-size: 1.05rem; color: var(--text-muted); margin-bottom: 16px; text-transform: uppercase; letter-spacing: 0.5px;">
            Recursos Opcionais & Melhorias
          </h3>

          <div class="onboarding-optional-grid">
            <div class="optional-feature-card">
              <div class="optional-icon">🔊</div>
              <div class="optional-content">
                <h4>FFmpeg (Opcional)</h4>
                <p>Identifica automaticamente faixas de áudio dublado/legendado e canais avançados. Se não tiver, o CineLocal usa detecção rápida.</p>
                <a href="https://ffmpeg.org/download.html" target="_blank" rel="noopener" class="optional-link">Baixar FFmpeg Oficial ➔</a>
              </div>
            </div>

            <div class="optional-feature-card">
              <div class="optional-icon">🍿</div>
              <div class="optional-content">
                <h4>VLC Media Player (Opcional)</h4>
                <p>Permite abrir vídeos com formatos avançados de cinema (TrueHD, DTS-HD, AC3 7.1) em 1 clique. O player web nativo é o padrão.</p>
                <a href="https://www.videolan.org/vlc/" target="_blank" rel="noopener" class="optional-link">Baixar VLC Oficial ➔</a>
              </div>
            </div>

            <div class="optional-feature-card">
              <div class="optional-icon">⚡</div>
              <div class="optional-content">
                <h4>Universo Marvel (MCU)</h4>
                <p>Ao adicionar produções da Marvel Studios, o CineLocal ativa automaticamente o Carrossel Cronológico e o Rastreador Canônico de 66 títulos.</p>
                <span style="font-size: 0.8rem; color: var(--text-muted);">Ativação automática por detecção</span>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    function addMarvelCarousel(container, title, items) {
      if (!items || items.length === 0) return;

      const sectionId = 'carousel_marvel';
      const section = document.createElement('section');
      section.className = 'carousel-section marvel-section';

      const totalMcu = (window.MCU_CANONICAL_TIMELINE || []).length || 66;
      let downloadedCount = 0;
      if (window.MCU_CANONICAL_TIMELINE) {
        window.MCU_CANONICAL_TIMELINE.forEach(entry => {
          if (findDownloadedMcuItem(entry)) downloadedCount++;
        });
      }
      if (downloadedCount === 0) downloadedCount = items.length;

      const percent = Math.round((downloadedCount / totalMcu) * 100);

      section.innerHTML = `
        <div class="carousel-header">
          <div class="carousel-title-box">
            <h3 class="carousel-title">${title}</h3>
            <span class="carousel-count">${items.length} títulos na sua coleção</span>
          </div>
          <button class="btn-mcu-timeline-header" onclick="openMcuTrackerModal()">
            <span class="pulse-dot"></span> Guia Cronológico Completo (66 Títulos) ➔
          </button>
        </div>
        <div class="carousel-track-wrapper">
          <button class="carousel-btn left" onclick="scrollTrack('${sectionId}', -600)">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
          </button>
          <div id="${sectionId}" class="carousel-track">
            <!-- Card de Destaque / Guia Cronológico -->
            <div class="movie-card mcu-hero-card" onclick="openMcuTrackerModal()" title="Abrir Linha do Tempo e Rastreador do MCU">
              <div class="card-poster-wrapper mcu-poster-wrapper">
                <div class="mcu-card-inner">
                  <div class="mcu-badge-top">GUIA CANÔNICO</div>
                  <div class="mcu-marvel-logo">MARVEL</div>
                  <div class="mcu-icon-orb">⚡</div>
                  <div class="mcu-stats-mini">
                    <span class="mcu-stat-num">${downloadedCount}/${totalMcu}</span>
                    <span class="mcu-stat-lbl">Títulos Disponíveis</span>
                  </div>
                  <div class="mcu-progress-container">
                    <div class="mcu-progress-bar" style="width: ${percent}%;"></div>
                  </div>
                </div>
              </div>
              <div class="card-content">
                <div>
                  <div class="card-title">Linha do Tempo MCU</div>
                  <div class="card-subinfo">66 Títulos • Cronologia Oficial</div>
                </div>
                <div class="card-actions">
                  <button class="card-btn-play mcu-btn-play" onclick="event.stopPropagation(); openMcuTrackerModal();">
                    Explorar Guia ⚡
                  </button>
                </div>
              </div>
            </div>
            ${items.map(item => createCardHtml(item, true)).join('')}
          </div>
          <button class="carousel-btn right" onclick="scrollTrack('${sectionId}', 600)">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </button>
        </div>
      `;

      container.appendChild(section);
    }

    function addCarousel(container, title, items, showSequenceBadge = false) {
      if (!items || items.length === 0) return;

      const sectionId = 'carousel_' + Math.random().toString(36).substr(2, 9);
      const section = document.createElement('section');
      section.className = 'carousel-section';

      section.innerHTML = `
        <div class="carousel-header">
          <div class="carousel-title-box">
            <h3 class="carousel-title">${title}</h3>
            <span class="carousel-count">${items.length} títulos</span>
          </div>
        </div>
        <div class="carousel-track-wrapper">
          <button class="carousel-btn left" onclick="scrollTrack('${sectionId}', -600)">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
          </button>
          <div id="${sectionId}" class="carousel-track">
            ${items.map(item => createCardHtml(item, showSequenceBadge)).join('')}
          </div>
          <button class="carousel-btn right" onclick="scrollTrack('${sectionId}', 600)">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </button>
        </div>
      `;

      container.appendChild(section);
    }

    function scrollTrack(trackId, amount) {
      const el = document.getElementById(trackId);
      if (el) el.scrollBy({ left: amount, behavior: 'smooth' });
    }

    function createCardHtml(item, showSeq = false) {
      const isSeries = item.type === 'series';
      const posterSrc = item.posterPath ? encodeURI(item.posterPath) : '';
      const qualityClass = isSeries ? 'badge-series' :
                           (item.resolution && item.resolution.includes('4K')) ? 'badge-4k' :
                           (item.resolution && item.resolution.includes('1080p')) ? 'badge-1080p' : 'badge-720p';

      const tagText = isSeries ? 'SÉRIE' : (item.resolution || 'HD');
      const clickAction = isSeries ? `openSeriesModal('${item.id}')` : `openMovieModal('${item.id}')`;
      const playAction = isSeries ? `openSeriesModal('${item.id}')` : `openPlayerById('${item.id}')`;
      
      const seqBadge = (showSeq && item.sequence) ? `<span class="badge-seq">#${String(item.sequence).padStart(2, '0')}</span>` : '';
      const audioBadge = item.audio ? `<span class="badge-tag badge-${item.audio.toLowerCase()}">${item.audio}</span>` : '';
      const subBadge = item.hasSubtitles ? `<span class="badge-tag badge-sub" title="Legenda disponível">CC</span>` : '';
      const subInfo = isSeries ? `${item.totalSeasons} Temporada • ${item.totalEpisodes} Eps` : `${item.year || ''} • ${item.format || ''}`;
      const audioLabelPart = item.audioLabel ? ` • ${item.audioLabel}` : '';

      const watched = isItemWatched(item.id);
      const watchedBadge = watched ? `<span class="card-watched-badge" title="Já assistido">✓ Assistido</span>` : '';

      const prog = getWatchProgress(item.id);
      let progressHtml = '';
      if (prog && prog.pct >= 2 && prog.pct < 92 && !prog.completed) {
        progressHtml = `<div class="card-progress-bar"><div class="card-progress-fill" style="width: ${prog.pct}%"></div></div>`;
      }

      return `
        <div class="movie-card dpad-focusable" tabindex="0" onclick="${clickAction}" data-id="${item.id}">
          <div class="card-poster-wrapper">
            <img class="card-poster" src="${posterSrc}" alt="${item.title}" loading="lazy" onerror="this.src='';">
            <span class="card-badge ${qualityClass}">${tagText}</span>
            ${seqBadge}
            ${watchedBadge}
            <div class="card-tag-group">
              ${audioBadge}
              ${subBadge}
            </div>
            ${progressHtml}
          </div>
          <div class="card-content">
            <div>
              <div class="card-title">${item.title}</div>
              <div class="card-subinfo">${subInfo}${audioLabelPart}</div>
            </div>
            <div class="card-actions">
              <button class="card-btn-play" onclick="event.stopPropagation(); ${playAction}">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                  <polygon points="5 3 19 12 5 21 5 3"></polygon>
                </svg>
                ${isSeries ? 'Episódios' : (prog && prog.pct >= 2 && !prog.completed ? 'Continuar' : 'Assistir')}
              </button>
              <button class="card-btn-fav" onclick="event.stopPropagation(); toggleFavorite('${item.id}')" title="${isItemFavorite(item.id) ? 'Remover da Minha Lista' : 'Adicionar à Minha Lista'}">
                ${isItemFavorite(item.id) ? '⭐' : '☆'}
              </button>
              ${(!isSeries && state.vlcAvailable) ? `
              <button class="card-btn-vlc" onclick="event.stopPropagation(); launchVlc('${item.videoPath}')" title="Assistir no VLC (Áudio 5.1)">
                VLC
              </button>` : ''}
              <button class="card-btn-info" onclick="event.stopPropagation(); ${clickAction}" title="Ver Sinopse e Detalhes">
                ℹ
              </button>
            </div>
          </div>
        </div>
      `;
    }

    /* RENDERIZAÇÃO DA GRADE DE FILMES */
    function populateGenreFilter() {
      const genreSet = new Set();
      state.movies.forEach(m => {
        if (m.genres && Array.isArray(m.genres)) {
          m.genres.forEach(g => genreSet.add(g));
        }
      });
      const sel = document.getElementById('genreSelectFilter');
      if (!sel) return;
      sel.innerHTML = '<option value="">Gênero: Todos</option>';
      Array.from(genreSet).sort().forEach(g => {
        const opt = document.createElement('option');
        opt.value = g;
        opt.innerText = g;
        sel.appendChild(opt);
      });
    }

    function setMovieGenreFilter(val) {
      state.genreFilter = val;
      renderMoviesGrid();
    }

    function setMovieYearFilter(val) {
      state.yearFilter = val;
      renderMoviesGrid();
    }

    function renderMoviesGrid() {
      const grid = document.getElementById('moviesGrid');
      if (state.movies.length === 0) {
        document.getElementById('moviesCountLabel').innerText = `0 títulos`;
        grid.innerHTML = `
          <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: var(--text-muted);">
            <div style="font-size: 3rem; margin-bottom: 16px;">📁</div>
            <h3 style="color: var(--text-main); margin-bottom: 8px;">Nenhum filme na pasta media/filmes</h3>
            <p style="max-width: 500px; margin: 0 auto 16px; line-height: 1.5;">Coloque seus filmes na pasta <code>media/filmes/Nome do Filme (Ano)/</code> e execute <strong>Atualizar Catalogo.bat</strong>.</p>
          </div>
        `;
        return;
      }

      let filtered = [...state.movies];

      // Busca Inteligente: Título, Franquia, Ano, Diretor, Elenco, Gêneros e Sinopse
      if (state.searchQuery) {
        const q = state.searchQuery.toLowerCase();
        filtered = filtered.filter(m => 
          (m.title && m.title.toLowerCase().includes(q)) || 
          (m.franchise && m.franchise.toLowerCase().includes(q)) || 
          (m.year && m.year.toString().includes(q)) ||
          (m.director && m.director.toLowerCase().includes(q)) ||
          (m.cast && m.cast.some(a => a.toLowerCase().includes(q))) ||
          (m.genres && m.genres.some(g => g.toLowerCase().includes(q))) ||
          (m.overview && m.overview.toLowerCase().includes(q))
        );
      }

      if (state.movieFilter === 'favorites') {
        filtered = filtered.filter(m => isItemFavorite(m.id));
      } else if (state.movieFilter === 'unwatched') {
        filtered = filtered.filter(m => !isItemWatched(m.id));
      } else if (state.movieFilter === 'franchise') {
        filtered = filtered.filter(m => m.franchise);
      } else if (state.movieFilter === 'standalone') {
        filtered = filtered.filter(m => !m.franchise);
      } else if (state.movieFilter === '4k') {
        filtered = filtered.filter(m => m.resolution && m.resolution.includes('4K'));
      } else if (state.movieFilter === '1080p') {
        filtered = filtered.filter(m => m.resolution && m.resolution.includes('1080p'));
      } else if (state.movieFilter === 'subtitled') {
        filtered = filtered.filter(m => m.subtitles && m.subtitles.length > 0);
      }

      if (state.genreFilter) {
        filtered = filtered.filter(m => m.genres && m.genres.includes(state.genreFilter));
      }

      if (state.yearFilter) {
        if (state.yearFilter === '2020') {
          filtered = filtered.filter(m => (m.year || 0) >= 2020);
        } else if (state.yearFilter === '2010') {
          filtered = filtered.filter(m => (m.year || 0) >= 2010 && (m.year || 0) <= 2019);
        } else if (state.yearFilter === '2000') {
          filtered = filtered.filter(m => (m.year || 0) >= 2000 && (m.year || 0) <= 2009);
        } else if (state.yearFilter === 'classic') {
          filtered = filtered.filter(m => (m.year || 0) < 2000);
        }
      }

      document.getElementById('moviesCountLabel').innerText = `${filtered.length} de ${state.movies.length} títulos`;
      grid.innerHTML = filtered.map(m => createCardHtml(m, false)).join('');
    }

    function setMovieFilter(filter) {
      state.movieFilter = filter;
      document.querySelectorAll('#moviesView .chip').forEach(c => {
        c.classList.toggle('active', c.dataset.filter === filter);
      });
      renderMoviesGrid();
    }

    /* RENDERIZAÇÃO DA GRADE DE SÉRIES */
    function renderSeriesGrid() {
      const grid = document.getElementById('seriesGrid');
      if (state.series.length === 0) {
        document.getElementById('seriesCountLabel').innerText = `0 séries`;
        grid.innerHTML = `
          <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: var(--text-muted);">
            <div style="font-size: 3rem; margin-bottom: 16px;">📺</div>
            <h3 style="color: var(--text-main); margin-bottom: 8px;">Nenhuma série na pasta media/series</h3>
            <p style="max-width: 500px; margin: 0 auto 16px; line-height: 1.5;">Coloque suas séries organizadas por temporadas (ex: <code>media/series/Nome/Season 01/</code>) e execute <strong>Atualizar Catalogo.bat</strong>.</p>
          </div>
        `;
        return;
      }
      let filtered = [...state.series];
      if (state.searchQuery) {
        const q = state.searchQuery.toLowerCase();
        filtered = filtered.filter(s => 
          (s.title && s.title.toLowerCase().includes(q)) || 
          (s.creator && s.creator.toLowerCase().includes(q)) || 
          (s.cast && s.cast.some(a => a.toLowerCase().includes(q))) || 
          (s.genres && s.genres.some(g => g.toLowerCase().includes(q))) || 
          (s.overview && s.overview.toLowerCase().includes(q))
        );
      }
      grid.innerHTML = filtered.map(s => createCardHtml(s, false)).join('');
      document.getElementById('seriesCountLabel').innerText = `${filtered.length} de ${state.series.length} séries disponíveis`;
    }

    /* MODAL DE SÉRIES */
    function openSeriesModal(seriesId) {
      const series = state.series.find(s => s.id === seriesId);
      if (!series) return;

      document.getElementById('seriesModalTitle').innerText = series.title;
      document.getElementById('seriesModalYear').innerText = series.year || '2024';
      document.getElementById('seriesModalSeasonsCount').innerText = `${series.totalSeasons || 1} Temporada(s)`;
      document.getElementById('seriesModalEpisodesCount').innerText = `${series.totalEpisodes} Episódios`;
      document.getElementById('seriesModalPoster').src = encodeURI(series.posterPath);

      // Metadados Ricos
      document.getElementById('seriesModalRating').innerHTML = series.rating ? `⭐ ${series.rating}` : '⭐ 8.0';
      
      const audioBadgeEl = document.getElementById('seriesModalAudioBadge');
      if (series.audio) {
        audioBadgeEl.style.display = 'inline-block';
        audioBadgeEl.className = `badge-tag badge-${series.audio.toLowerCase()}`;
        audioBadgeEl.innerText = series.audio;
      } else {
        audioBadgeEl.style.display = 'none';
      }

      const subBadgeEl = document.getElementById('seriesModalSubBadge');
      subBadgeEl.style.display = series.hasSubtitles ? 'inline-block' : 'none';

      // Gêneros
      const genresEl = document.getElementById('seriesModalGenres');
      if (series.genres && series.genres.length > 0) {
        genresEl.innerHTML = series.genres.map(g => `<span class="genre-pill">${g}</span>`).join('');
      } else {
        genresEl.innerHTML = '<span class="genre-pill">Série</span><span class="genre-pill">Drama</span>';
      }

      // Sinopse oficial (dinâmica para CADA série!)
      document.getElementById('seriesModalDesc').innerText = series.overview || 'Sinopse não disponível.';

      // Créditos
      document.getElementById('seriesModalCreator').innerHTML = series.creator ? `<strong>Criação:</strong> ${series.creator}` : '';
      document.getElementById('seriesModalCast').innerHTML = (series.cast && series.cast.length > 0) ? `<strong>Elenco:</strong> ${series.cast.join(', ')}` : '';

      // Links externos
      const linksEl = document.getElementById('seriesModalLinks');
      let linksHtml = '';
      if (series.tmdbUrl) {
        linksHtml += `<a href="${series.tmdbUrl}" target="_blank" rel="noopener" class="btn-external-link tmdb">Ficha no TMDb ↗</a>`;
      }
      if (series.imdbUrl) {
        linksHtml += `<a href="${series.imdbUrl}" target="_blank" rel="noopener" class="btn-external-link imdb">Ficha no IMDb ↗</a>`;
      }
      linksEl.innerHTML = linksHtml;

      // Botão de Já Assistido
      const seriesWatchedBtn = document.getElementById('seriesModalBtnWatched');
      if (seriesWatchedBtn) {
        const isWatched = isItemWatched(series.id);
        seriesWatchedBtn.classList.toggle('active', isWatched);
        seriesWatchedBtn.innerText = isWatched ? '✓ Já Assistido' : '✓ Marcar como Assistido';
      }

      // Botão de Minha Lista
      const seriesFavBtn = document.getElementById('seriesModalBtnFavorite');
      if (seriesFavBtn) {
        const isFav = isItemFavorite(series.id);
        seriesFavBtn.classList.toggle('active', isFav);
        seriesFavBtn.innerText = isFav ? '⭐ Na Minha Lista' : '⭐ Minha Lista';
      }

      // Renderizar Tabs de Temporadas
      const tabs = document.getElementById('seriesSeasonsTabs');
      tabs.innerHTML = series.seasons.map((s, idx) => `
        <button class="season-tab ${idx === 0 ? 'active' : ''}" onclick="selectSeason('${series.id}', ${idx})">
          ${s.title}
        </button>
      `).join('');

      renderSeasonEpisodes(series, 0);

      document.getElementById('seriesModal').classList.add('active');
      document.body.style.overflow = 'hidden';
    }

    function toggleWatchedCurrentSeries() {
      const title = document.getElementById('seriesModalTitle').innerText;
      const series = state.series.find(s => s.title === title || s.id === title);
      if (series) {
        toggleWatched(series.id);
        const watched = isItemWatched(series.id);
        const btn = document.getElementById('seriesModalBtnWatched');
        if (btn) {
          btn.classList.toggle('active', watched);
          btn.innerText = watched ? '✓ Já Assistido' : '✓ Marcar como Assistido';
        }
      }
    }

    /* MODAL DE FILMES */
    let currentModalMovie = null;

    function openMovieModal(movieId) {
      const movie = state.movies.find(m => m.id === movieId);
      if (!movie) return;
      currentModalMovie = movie;

      document.getElementById('movieModalTitle').innerText = movie.title;
      document.getElementById('movieModalYear').innerText = movie.year || '';
      document.getElementById('movieModalRes').innerText = movie.resolution || 'HD';
      document.getElementById('movieModalFormat').innerText = movie.format || 'MKV';
      document.getElementById('movieModalSize').innerText = movie.sizeFormatted || '';
      document.getElementById('movieModalPoster').src = movie.posterPath ? encodeURI(movie.posterPath) : '';

      // Metadados Ricos
      document.getElementById('movieModalRating').innerHTML = movie.rating ? `⭐ ${movie.rating}` : '⭐ 7.5';

      const audioBadgeEl = document.getElementById('movieModalAudioBadge');
      if (movie.audio) {
        audioBadgeEl.style.display = 'inline-block';
        audioBadgeEl.className = `badge-tag badge-${movie.audio.toLowerCase()}`;
        audioBadgeEl.innerText = movie.audio;
      } else {
        audioBadgeEl.style.display = 'none';
      }

      const subBadgeEl = document.getElementById('movieModalSubBadge');
      subBadgeEl.style.display = movie.hasSubtitles ? 'inline-block' : 'none';

      // Gêneros
      const genresEl = document.getElementById('movieModalGenres');
      if (movie.genres && movie.genres.length > 0) {
        genresEl.innerHTML = movie.genres.map(g => `<span class="genre-pill">${g}</span>`).join('');
      } else {
        genresEl.innerHTML = '<span class="genre-pill">Filme</span><span class="genre-pill">Cinema</span>';
      }

      // Sinopse
      document.getElementById('movieModalDesc').innerText = movie.overview || 'Sinopse não disponível.';

      // Créditos
      document.getElementById('movieModalDirector').innerHTML = movie.director ? `<strong>Direção:</strong> ${movie.director}` : '';
      document.getElementById('movieModalCast').innerHTML = (movie.cast && movie.cast.length > 0) ? `<strong>Elenco:</strong> ${movie.cast.join(', ')}` : '';

      // Links externos
      const linksEl = document.getElementById('movieModalLinks');
      let linksHtml = '';
      if (movie.tmdbUrl) {
        linksHtml += `<a href="${movie.tmdbUrl}" target="_blank" rel="noopener" class="btn-external-link tmdb">Ficha no TMDb ↗</a>`;
      }
      if (movie.imdbUrl) {
        linksHtml += `<a href="${movie.imdbUrl}" target="_blank" rel="noopener" class="btn-external-link imdb">Ficha no IMDb ↗</a>`;
      }
      linksEl.innerHTML = linksHtml;

      const vlcBtn = document.getElementById('movieModalBtnVlc');
      if (vlcBtn) vlcBtn.style.display = state.vlcAvailable ? 'inline-flex' : 'none';

      // Continuar assistindo / Retomar no modal
      const resumeBtn = document.getElementById('movieModalBtnResume');
      const prog = getWatchProgress(movie.id);
      if (resumeBtn) {
        if (prog && prog.currentTime > 15 && !prog.completed) {
          resumeBtn.style.display = 'inline-flex';
          resumeBtn.innerText = `⏱️ Continuar de ${formatTime(prog.currentTime)}`;
        } else {
          resumeBtn.style.display = 'none';
        }
      }

      // Já assistido status
      const watchedBtn = document.getElementById('movieModalBtnWatched');
      if (watchedBtn) {
        const watched = isItemWatched(movie.id);
        watchedBtn.classList.toggle('active', watched);
        watchedBtn.innerText = watched ? '✓ Já Assistido' : '✓ Marcar como Assistido';
      }

      // Minha Lista status
      const favBtn = document.getElementById('movieModalBtnFavorite');
      if (favBtn) {
        const isFav = isItemFavorite(movie.id);
        favBtn.classList.toggle('active', isFav);
        favBtn.innerText = isFav ? '⭐ Na Minha Lista' : '⭐ Minha Lista';
      }

      document.getElementById('movieDetailsModal').classList.add('active');
      document.body.style.overflow = 'hidden';
    }

    function closeMovieModal() {
      document.getElementById('movieDetailsModal').classList.remove('active');
      document.body.style.overflow = 'auto';
      currentModalMovie = null;
    }

    function closeMovieModalOnOut(e) {
      if (e.target.id === 'movieDetailsModal') {
        closeMovieModal();
      }
    }

    function playMovieFromModal() {
      if (currentModalMovie) {
        const mov = currentModalMovie;
        closeMovieModal();
        openPlayer(mov, false);
      }
    }

    function resumeMovieFromModal() {
      if (currentModalMovie) {
        const mov = currentModalMovie;
        const prog = getWatchProgress(mov.id);
        closeMovieModal();
        openPlayer(mov, false, prog ? prog.currentTime : 0);
      }
    }

    function toggleWatchedCurrentMovie() {
      if (currentModalMovie) {
        toggleWatched(currentModalMovie.id);
        const watched = isItemWatched(currentModalMovie.id);
        const btn = document.getElementById('movieModalBtnWatched');
        if (btn) {
          btn.classList.toggle('active', watched);
          btn.innerText = watched ? '✓ Já Assistido' : '✓ Marcar como Assistido';
        }
      }
    }

    function vlcMovieFromModal() {
      if (currentModalMovie) {
        launchVlc(currentModalMovie.videoPath);
      }
    }

    function selectSeason(seriesId, seasonIdx) {
      const series = state.series.find(s => s.id === seriesId);
      if (!series) return;
      document.querySelectorAll('#seriesSeasonsTabs .season-tab').forEach((t, i) => {
        t.classList.toggle('active', i === seasonIdx);
      });
      renderSeasonEpisodes(series, seasonIdx);
    }

    function renderSeasonEpisodes(series, seasonIdx) {
      const season = series.seasons[seasonIdx];
      const list = document.getElementById('seriesEpisodesList');
      if (!season) return;

      list.innerHTML = season.episodes.map(ep => {
        const epAudioBadge = ep.audio ? `<span class="badge-tag badge-${ep.audio.toLowerCase()}">${ep.audio}</span>` : '';
        const epSubBadge = ep.hasSubtitles ? `<span class="badge-tag badge-sub">CC</span>` : '';
        const epAudioLabel = ep.audioLabel ? ` • ${ep.audioLabel}` : '';

        return `
        <div class="episode-card" onclick="playEpisode('${series.id}', ${seasonIdx}, ${ep.episodeNumber})">
          <div class="episode-left">
            <div class="episode-num">E${String(ep.episodeNumber).padStart(2, '0')}</div>
            <div class="episode-title-box">
              <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
                <h4>${ep.title}</h4>
                ${epAudioBadge}
                ${epSubBadge}
              </div>
              <p>${ep.resolution} • ${ep.format} • ${ep.sizeFormatted}${epAudioLabel}</p>
            </div>
          </div>
          <div class="episode-actions">
            <button class="card-btn-play" onclick="event.stopPropagation(); playEpisode('${series.id}', ${seasonIdx}, ${ep.episodeNumber})">
              ▶ Assistir
            </button>
            ${state.vlcAvailable ? `
            <button class="card-btn-vlc" onclick="event.stopPropagation(); launchVlc('${ep.videoPath}')">
              VLC
            </button>` : ''}
          </div>
        </div>
      `;
      }).join('');
    }

    function closeSeriesModal() {
      document.getElementById('seriesModal').classList.remove('active');
      document.body.style.overflow = '';
    }

    function closeSeriesModalOnOut(e) {
      if (e.target.id === 'seriesModal') closeSeriesModal();
    }

    /* ============================================================= */
    /* LINHA DO TEMPO CANÔNICA DO MCU & RASTREADOR (66 PRODUÇÕES)   */
    /* ============================================================= */
    window.MCU_CANONICAL_TIMELINE = [
      { seq: 1, title: 'Capitão América: O Primeiro Vingador', year: 2011, type: 'movie', note: 'se passa na década de 1940', keywords: ['primeiro vingador', 'first avenger'] },
      { seq: 2, title: 'Capitã Marvel', year: 2019, type: 'movie', note: 'se passa em 1995', keywords: ['capitã marvel', 'captain marvel'] },
      { seq: 3, title: 'Homem de Ferro', year: 2008, type: 'movie', note: 'o nascimento do MCU', keywords: ['homem de ferro (2008)', 'iron man (2008)'] },
      { seq: 4, title: 'Homem de Ferro 2', year: 2010, type: 'movie', note: 'se passa meses após o primeiro em 2010', keywords: ['homem de ferro 2', 'iron man 2'] },
      { seq: 5, title: 'O Incrível Hulk', year: 2008, type: 'movie', note: 'se passa simultaneamente a Homem de Ferro 2 e Thor', keywords: ['incrível hulk', 'incredible hulk'] },
      { seq: 6, title: 'Thor', year: 2011, type: 'movie', note: 'se passa simultaneamente a Homem de Ferro 2 e Hulk', keywords: ['thor (2011)'] },
      { seq: 7, title: 'Os Vingadores', year: 2012, type: 'movie', note: 'a Batalha de Nova York', keywords: ['os vingadores', 'the avengers (2012)'] },
      { seq: 8, title: 'Thor: O Mundo Sombrio', year: 2013, type: 'movie', note: 'consequências em Asgard e Joia da Realidade', keywords: ['mundo sombrio', 'dark world'] },
      { seq: 9, title: 'Homem de Ferro 3', year: 2013, type: 'movie', note: 'traumas pós-Nova York no Natal de 2012', keywords: ['homem de ferro 3', 'iron man 3'] },
      { seq: 10, title: 'Capitão América 2: O Soldado Invernal', year: 2014, type: 'movie', note: 'a queda da S.H.I.E.L.D. e ascensão da Hidra', keywords: ['soldado invernal', 'winter soldier'] },
      { seq: 11, title: 'Guardiões da Galáxia', year: 2014, type: 'movie', note: 'no cosmos em 2014, Joia do Poder', keywords: ['guardiões da galáxia (2014)', 'guardioes da galaxia (2014)', 'guardians of the galaxy (2014)'] },
      { seq: 12, title: 'Guardiões da Galáxia Vol. 2', year: 2017, type: 'movie', note: 'se passa meses após o primeiro em 2014', keywords: ['guardiões da galáxia vol. 2', 'guardioes da galaxia vol. 2', 'guardians of the galaxy vol. 2'] },
      { seq: 13, title: 'Eu Sou Groot — Temporadas 1 e 2', year: 2022, type: 'series', note: 'curtas espaciais do Baby Groot', keywords: ['eu sou groot', 'i am groot'] },
      { seq: 14, title: 'Demolidor — 1ª Temporada', year: 2015, type: 'series', note: 'Hell\'s Kitchen em 2015', keywords: ['demolidor', 'daredevil'] },
      { seq: 15, title: 'Jessica Jones — 1ª Temporada', year: 2015, type: 'series', note: 'confronto com Kilgrave', keywords: ['jessica jones'] },
      { seq: 16, title: 'Vingadores: Era de Ultron', year: 2015, type: 'movie', note: 'nascimento de Visão e destruição de Sokovia', keywords: ['era de ultron', 'age of ultron'] },
      { seq: 17, title: 'Homem-Formiga', year: 2015, type: 'movie', note: 'Scott Lang e o Reino Quântico', keywords: ['homem-formiga (2015)', 'ant-man (2015)'] },
      { seq: 18, title: 'Demolidor — 2ª Temporada', year: 2016, type: 'series', note: 'conflito com o Justiceiro e Elektra', keywords: ['demolidor', 'daredevil'] },
      { seq: 19, title: 'Luke Cage — 1ª Temporada', year: 2016, type: 'series', note: 'Harlem em 2016', keywords: ['luke cage'] },
      { seq: 20, title: 'Punho de Ferro — 1ª Temporada', year: 2017, type: 'series', note: 'o retorno de Danny Rand e o Tentáculo', keywords: ['punho de ferro', 'iron fist'] },
      { seq: 21, title: 'Os Defensores', year: 2017, type: 'series', note: 'união dos heróis das ruas de Nova York', keywords: ['os defensores', 'the defenders'] },
      { seq: 22, title: 'Capitão América: Guerra Civil', year: 2016, type: 'movie', note: 'Acordos de Sokovia e o racha dos Vingadores', keywords: ['guerra civil', 'civil war'] },
      { seq: 23, title: 'Viúva Negra', year: 2021, type: 'movie', note: 'se passa logo após Guerra Civil em 2016', keywords: ['viúva negra', 'viuva negra', 'black widow'] },
      { seq: 24, title: 'Pantera Negra', year: 2018, type: 'movie', note: 'se passa semanas após Guerra Civil em 2016', keywords: ['pantera negra (2018)', 'black panther (2018)'] },
      { seq: 25, title: 'Homem-Aranha: De Volta ao Lar', year: 2017, type: 'movie', note: 'se passa meses após Guerra Civil em 2016', keywords: ['de volta ao lar', 'homecoming'] },
      { seq: 26, title: 'O Justiceiro — 1ª Temporada', year: 2017, type: 'series', note: 'conspiração militar e vingança', keywords: ['o justiceiro', 'the punisher'] },
      { seq: 27, title: 'Doutor Estranho', year: 2016, type: 'movie', note: 'começa em 2016 e termina em 2017', keywords: ['doutor estranho (2016)', 'doctor strange (2016)'] },
      { seq: 28, title: 'Jessica Jones — 2ª Temporada', year: 2018, type: 'series', note: 'origens dos poderes e a IGH', keywords: ['jessica jones'] },
      { seq: 29, title: 'Luke Cage — 2ª Temporada', year: 2018, type: 'series', note: 'disputa pelo império do Harlem', keywords: ['luke cage'] },
      { seq: 30, title: 'Punho de Ferro — 2ª Temporada', year: 2018, type: 'series', note: 'guerra de gangues em Chinatown', keywords: ['punho de ferro', 'iron fist'] },
      { seq: 31, title: 'Demolidor — 3ª Temporada', year: 2018, type: 'series', note: 'retorno implacável do Rei do Crime', keywords: ['demolidor', 'daredevil'] },
      { seq: 32, title: 'Thor: Ragnarok', year: 2017, type: 'movie', note: 'destruição de Asgard e fuga pelo espaço', keywords: ['ragnarok'] },
      { seq: 33, title: 'O Justiceiro — 2ª Temporada', year: 2019, type: 'series', note: 'Frank Castle em fuga pelas estradas', keywords: ['o justiceiro', 'the punisher'] },
      { seq: 34, title: 'Jessica Jones — 3ª Temporada', year: 2019, type: 'series', note: 'confronto psicológico final', keywords: ['jessica jones'] },
      { seq: 35, title: 'Homem-Formiga e a Vespa', year: 2018, type: 'movie', note: 'resgate no Reino Quântico durante o estalo', keywords: ['homem-formiga e a vespa', 'ant-man and the wasp (2018)'] },
      { seq: 36, title: 'Vingadores: Guerra Infinita', year: 2018, type: 'movie', note: 'Thanos e o estalar de dedos com as Joias', keywords: ['guerra infinita', 'infinity war'] },
      { seq: 37, title: 'Vingadores: Ultimato', year: 2019, type: 'movie', note: 'salto temporal terminando em 2023', keywords: ['ultimato', 'endgame'] },
      { seq: 38, title: 'Loki — Temporada 1', year: 2021, type: 'series', note: 'linha temporal ramificada imediatamente após 2012 em Ultimato', keywords: ['loki'] },
      { seq: 39, title: 'What If...? — Temporadas 1, 2 e 3', year: 2021, type: 'series', note: 'multiverso ramificado pós-Loki com o Vigia', keywords: ['what if'] },
      { seq: 40, title: 'WandaVision', year: 2021, type: 'series', note: 'se passa semanas após Ultimato em 2023', keywords: ['wandavision'] },
      { seq: 41, title: 'Shang-Chi e a Lenda dos Dez Anéis', year: 2021, type: 'movie', note: 'se passa em 2024, artes marciais místicas', keywords: ['shang-chi', 'dez anéis', 'ten rings'] },
      { seq: 42, title: 'Falcão e o Soldado Invernal', year: 2021, type: 'series', note: 'se passa em 2024, o legado do escudo', keywords: ['falcão e o soldado invernal', 'falcon and the winter soldier'] },
      { seq: 43, title: 'Homem-Aranha: Longe de Casa', year: 2019, type: 'movie', note: 'se passa em 2024, viagem escolar na Europa', keywords: ['longe de casa', 'far from home'] },
      { seq: 44, title: 'Eternos', year: 2021, type: 'movie', note: 'se passa em 2024, o despertar dos Celestiais', keywords: ['eternos', 'eternals'] },
      { seq: 45, title: 'Homem-Aranha: Sem Volta Para Casa', year: 2021, type: 'movie', note: 'se passa no final de 2024, fenda no multiverso', keywords: ['sem volta para casa', 'no way home'] },
      { seq: 46, title: 'Doutor Estranho no Multiverso da Loucura', year: 2022, type: 'movie', note: 'se passa entre 2024 e 2025, fuga pelo multiverso', keywords: ['multiverso da loucura', 'multiverse of madness'] },
      { seq: 47, title: 'Gavião Arqueiro', year: 2021, type: 'series', note: 'Natal de 2024 em Nova York', keywords: ['gavião arqueiro', 'hawkeye'] },
      { seq: 48, title: 'Cavaleiro da Lua', year: 2022, type: 'series', note: 'se passa em 2025, deuses egípcios', keywords: ['cavaleiro da lua', 'moon knight'] },
      { seq: 49, title: 'Pantera Negra: Wakanda Para Sempre', year: 2022, type: 'movie', note: 'se passa em 2025, conflito com Namor', keywords: ['wakanda para sempre', 'wakanda forever'] },
      { seq: 50, title: 'Eco', year: 2024, type: 'series', note: 'se passa em 2025, origens e retorno à terra natal', keywords: ['eco (2024)', 'echo (2024)'] },
      { seq: 51, title: 'Mulher-Hulk: Defensora de Heróis', year: 2022, type: 'series', note: 'se passa em 2025, direito sobre-humano', keywords: ['mulher-hulk', 'she-hulk'] },
      { seq: 52, title: 'Ms. Marvel', year: 2022, type: 'series', note: 'se passa em 2025, Kamala Khan em Jersey City', keywords: ['ms. marvel', 'ms marvel'] },
      { seq: 53, title: 'Thor: Amor e Trovão', year: 2022, type: 'movie', note: 'se passa em 2025, Gorr o Carniceiro dos Deuses', keywords: ['amor e trovão', 'love and thunder'] },
      { seq: 54, title: 'Lobisomem na Noite', year: 2022, type: 'movie', note: 'especial macabro de 2025 em preto e branco', keywords: ['lobisomem na noite', 'werewolf by night'] },
      { seq: 55, title: 'Guardiões da Galáxia: Especial de Festas', year: 2022, type: 'movie', note: 'final de 2025 em Luganenhum', keywords: ['especial de festas', 'holiday special'] },
      { seq: 56, title: 'Homem-Formiga e a Vespa: Quantumania', year: 2023, type: 'movie', note: 'se passa em 2026, Kang o Conquistador', keywords: ['quantumania'] },
      { seq: 57, title: 'Guardiões da Galáxia Vol. 3', year: 2023, type: 'movie', note: 'se passa em 2026, resgate de Rocket Raccoon', keywords: ['guardiões da galáxia vol. 3', 'guardioes da galaxia vol. 3', 'guardians of the galaxy vol. 3'] },
      { seq: 58, title: 'Invasão Secreta', year: 2023, type: 'series', note: 'se passa em 2026, infiltração Skrull na Terra', keywords: ['invasão secreta', 'secret invasion'] },
      { seq: 59, title: 'As Marvels', year: 2023, type: 'movie', note: 'se passa em 2026, emaranhamento quântico cósmico', keywords: ['as marvels', 'the marvels'] },
      { seq: 60, title: 'Loki — Temporada 2', year: 2023, type: 'series', note: 'desfecho do trono temporal do multiverso e Yggdrasil', keywords: ['loki'] },
      { seq: 61, title: 'Deadpool & Wolverine', year: 2024, type: 'movie', note: 'TVA e linhas do tempo após Loki', keywords: ['deadpool & wolverine', 'deadpool e wolverine'] },
      { seq: 62, title: 'Agatha Desde Sempre', year: 2024, type: 'series', note: 'desdobramento místico de WandaVision no Caminho das Bruxas', keywords: ['agatha desde sempre', 'agatha all along'] },
      { seq: 63, title: 'Demolidor: Renascido — 1ª Temporada', year: 2025, type: 'series', note: 'o novo capítulo de Matt Murdock no MCU', keywords: ['demolidor: renascido', 'daredevil: born again'] },
      { seq: 64, title: 'Capitão América: Admirável Mundo Novo', year: 2025, type: 'movie', note: 'Sam Wilson e a conspiração da Casa Branca', keywords: ['admirável mundo novo', 'admiravel mundo novo', 'brave new world'] },
      { seq: 65, title: 'Thunderbolts*', year: 2025, type: 'movie', note: 'a equipe de anti-heróis clandestinos do governo', keywords: ['thunderbolts'] },
      { seq: 66, title: 'Quarteto Fantástico: Primeiros Passos', year: 2025, type: 'movie', note: 'universo alternativo nos anos 1960 convergindo ao MCU', keywords: ['quarteto fantástico', 'quarteto fantastico', 'fantastic four'] }
    ];

    let currentMcuFilter = 'all';
    let currentMcuSearch = '';

    function findDownloadedMcuItem(entry) {
      const list = state.all || state.catalogo || window.CATALOGO || [];
      if (!list || list.length === 0) return null;
      for (const item of list) {
        const fullStr = (item.title + ' ' + (item.rawName || '') + ' ' + (item.folder || '')).toLowerCase();
        for (const kw of entry.keywords) {
          if (fullStr.includes(kw.toLowerCase())) {
            // For series like Loki or WandaVision, ensure correct type
            if (entry.type === 'series' && item.type === 'series') return item;
            if (entry.type === 'movie' && item.type === 'movie') return item;
            if (entry.type === 'series' && fullStr.includes(kw.toLowerCase())) return item;
            if (entry.type === 'movie' && fullStr.includes(kw.toLowerCase())) return item;
          }
        }
      }
      return null;
    }

    function openMcuTrackerModal() {
      const modal = document.getElementById('mcuTrackerModal');
      if (!modal) return;
      
      currentMcuFilter = 'all';
      currentMcuSearch = '';
      const searchInp = document.getElementById('mcuSearchInput');
      if (searchInp) searchInp.value = '';
      
      document.querySelectorAll('.mcu-chip').forEach(c => {
        c.classList.toggle('active', c.getAttribute('data-filter') === 'all');
      });

      updateMcuStats();
      renderMcuTrackerList();
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
    }

    function closeMcuTrackerModal() {
      const modal = document.getElementById('mcuTrackerModal');
      if (modal) modal.classList.remove('active');
      document.body.style.overflow = '';
    }

    function closeMcuTrackerOnOut(e) {
      if (e.target.id === 'mcuTrackerModal') {
        closeMcuTrackerModal();
      }
    }

    function updateMcuStats() {
      const total = window.MCU_CANONICAL_TIMELINE.length;
      let downloaded = 0;
      window.MCU_CANONICAL_TIMELINE.forEach(entry => {
        if (findDownloadedMcuItem(entry)) downloaded++;
      });
      const missing = total - downloaded;
      const pct = Math.round((downloaded / total) * 100);

      const elTot = document.getElementById('mcuStatTotal');
      const elDown = document.getElementById('mcuStatDownloaded');
      const elMiss = document.getElementById('mcuStatMissing');
      const elPct = document.getElementById('mcuStatPercent');
      const elProg = document.getElementById('mcuProgressLargeFill');
      const chipDown = document.getElementById('mcuChipDownloadedCount');
      const chipMiss = document.getElementById('mcuChipMissingCount');

      if (elTot) elTot.innerText = total;
      if (elDown) elDown.innerText = downloaded;
      if (elMiss) elMiss.innerText = missing;
      if (elPct) elPct.innerText = pct + '%';
      if (elProg) elProg.style.width = pct + '%';
      if (chipDown) chipDown.innerText = downloaded;
      if (chipMiss) chipMiss.innerText = missing;
    }

    function setMcuFilter(filterName) {
      currentMcuFilter = filterName;
      document.querySelectorAll('.mcu-chip').forEach(c => {
        c.classList.toggle('active', c.getAttribute('data-filter') === filterName);
      });
      renderMcuTrackerList();
    }

    function filterMcuList() {
      const searchInp = document.getElementById('mcuSearchInput');
      currentMcuSearch = (searchInp ? searchInp.value : '').toLowerCase().trim();
      renderMcuTrackerList();
    }

    function renderMcuTrackerList() {
      const listEl = document.getElementById('mcuTimelineList');
      if (!listEl) return;

      const items = window.MCU_CANONICAL_TIMELINE.filter(entry => {
        const itemMatch = findDownloadedMcuItem(entry);
        const isDownloaded = !!itemMatch;

        // Filtro de status / tipo
        if (currentMcuFilter === 'downloaded' && !isDownloaded) return false;
        if (currentMcuFilter === 'missing' && isDownloaded) return false;
        if (currentMcuFilter === 'movie' && entry.type !== 'movie') return false;
        if (currentMcuFilter === 'series' && entry.type !== 'series') return false;

        // Filtro de busca
        if (currentMcuSearch) {
          const matchTitle = entry.title.toLowerCase().includes(currentMcuSearch);
          const matchNote = entry.note.toLowerCase().includes(currentMcuSearch);
          const matchYear = String(entry.year).includes(currentMcuSearch);
          if (!matchTitle && !matchNote && !matchYear) return false;
        }

        return true;
      });

      if (items.length === 0) {
        listEl.innerHTML = `
          <div style="text-align: center; padding: 40px 20px; color: var(--text-muted);">
            <div style="font-size: 32px; margin-bottom: 8px;">🔍</div>
            <p>Nenhum título encontrado com os filtros selecionados.</p>
          </div>
        `;
        return;
      }

      listEl.innerHTML = items.map(entry => {
        const itemMatch = findDownloadedMcuItem(entry);
        const isDown = !!itemMatch;
        const seqStr = '#' + String(entry.seq).padStart(2, '0');
        const typeBadge = entry.type === 'series' 
          ? '<span class="mcu-type-badge series">Série</span>' 
          : '<span class="mcu-type-badge movie">Filme</span>';

        let statusTag = '';
        let actionBtn = '';

        if (isDown) {
          const res = itemMatch.resolution ? ` • ${itemMatch.resolution}` : '';
          const aud = itemMatch.audio ? ` • ${itemMatch.audio}` : '';
          statusTag = `<span class="mcu-status-tag downloaded">✓ NA COLEÇÃO${res}${aud}</span>`;
          
          if (itemMatch.type === 'series') {
            actionBtn = `<button class="btn-mcu-play series" onclick="playMcuItem('${itemMatch.id}', 'series')">Ver Episódios 📺</button>`;
          } else {
            actionBtn = `<button class="btn-mcu-play" onclick="playMcuItem('${itemMatch.id}', 'movie')">Assistir ▶</button>`;
          }
        } else {
          if (entry.year >= 2025) {
            statusTag = `<span class="mcu-status-tag future">EM BREVE (${entry.year})</span>`;
          } else {
            statusTag = `<span class="mcu-status-tag missing">NÃO BAIXADO</span>`;
          }
        }

        return `
          <div class="mcu-timeline-item ${isDown ? 'downloaded' : 'missing'}">
            <div class="mcu-item-seq">${seqStr}</div>
            <div class="mcu-item-info">
              <div class="mcu-item-title-row">
                <span class="mcu-item-title">${entry.title}</span>
                <span class="mcu-item-year">(${entry.year})</span>
                ${typeBadge}
              </div>
              <div class="mcu-item-note">⚡ ${entry.note}</div>
            </div>
            <div class="mcu-item-actions">
              ${statusTag}
              ${actionBtn}
            </div>
          </div>
        `;
      }).join('');
    }

    function playMcuItem(itemId, itemType) {
      closeMcuTrackerModal();
      if (itemType === 'series') {
        openSeriesModal(itemId);
      } else {
        openPlayerById(itemId);
      }
    }

    /* PLAYER & REPRODUÇÃO */
    let nextEpCountdownTimer = null;
    const SPEED_OPTIONS = [0.75, 1.0, 1.25, 1.5, 2.0];

    function openPlayerById(movieId, startTime = 0) {
      const movie = state.movies.find(m => m.id === movieId);
      if (movie) openPlayer(movie, false, startTime);
    }

    function playEpisode(seriesId, seasonIdx, epNum, startTime = 0) {
      const series = state.series.find(s => s.id === seriesId);
      if (!series) return;
      const season = series.seasons[seasonIdx];
      if (!season) return;
      const ep = season.episodes.find(e => e.episodeNumber === epNum);
      if (!ep) return;

      closeSeriesModal();
      state.currentEpisodeSeries = { series, seasonIdx, epNum };
      openPlayer(ep, true, startTime);
    }

    function getNextEpisode() {
      if (!state.currentEpisodeSeries) return null;
      const { series, seasonIdx, epNum } = state.currentEpisodeSeries;
      const season = series.seasons[seasonIdx];
      if (!season) return null;
      const nextEp = season.episodes.find(e => e.episodeNumber === epNum + 1);
      if (nextEp) return { series, seasonIdx, episode: nextEp };
      // Próxima temporada
      if (series.seasons[seasonIdx + 1] && series.seasons[seasonIdx + 1].episodes.length > 0) {
        return { series, seasonIdx: seasonIdx + 1, episode: series.seasons[seasonIdx + 1].episodes[0] };
      }
      return null;
    }

    function playNextEpisode() {
      const nextInfo = getNextEpisode();
      if (nextInfo) {
        showToast(`Iniciando Episódio ${nextInfo.episode.episodeNumber}...`);
        playEpisode(nextInfo.series.id, nextInfo.seasonIdx, nextInfo.episode.episodeNumber);
      } else {
        showToast('Fim dos episódios desta temporada!');
      }
    }

    function startNextEpisodeCountdown(initialSecs) {
      const nextInfo = getNextEpisode();
      if (!nextInfo) return;

      state.nextEpCountdownActive = true;
      let countdown = Math.min(20, Math.max(5, initialSecs));

      const toast = document.getElementById('nextEpisodeToast');
      const countEl = document.getElementById('nextEpCountdown');
      const titleEl = document.getElementById('nextEpTitle');

      if (titleEl) titleEl.innerText = `${nextInfo.series.title} • E${String(nextInfo.episode.episodeNumber).padStart(2,'0')} - ${nextInfo.episode.title}`;
      if (countEl) countEl.innerText = countdown;
      if (toast) toast.style.display = 'flex';

      clearInterval(nextEpCountdownTimer);
      nextEpCountdownTimer = setInterval(() => {
        countdown--;
        if (countEl) countEl.innerText = countdown;
        if (countdown <= 0) {
          clearInterval(nextEpCountdownTimer);
          state.nextEpCountdownActive = false;
          if (toast) toast.style.display = 'none';
          playNextEpisodeImmediately();
        }
      }, 1000);
    }

    function dismissNextEpisodeCountdown() {
      clearInterval(nextEpCountdownTimer);
      state.nextEpCountdownActive = false;
      state.nextEpDismissed = true;
      const toast = document.getElementById('nextEpisodeToast');
      if (toast) toast.style.display = 'none';
    }

    function playNextEpisodeImmediately() {
      clearInterval(nextEpCountdownTimer);
      state.nextEpCountdownActive = false;
      state.nextEpDismissed = false;
      const toast = document.getElementById('nextEpisodeToast');
      if (toast) toast.style.display = 'none';

      const nextInfo = getNextEpisode();
      if (nextInfo) {
        showToast(`Iniciando Episódio ${nextInfo.episode.episodeNumber}...`);
        playEpisode(nextInfo.series.id, nextInfo.seasonIdx, nextInfo.episode.episodeNumber);
      } else {
        showToast('Fim da temporada!');
      }
    }

    /* FEEDBACK CENTRAL (ESTILO YOUTUBE) */
    function showCenterPulse(action) {
      const fb = document.getElementById('playerCenterFeedback');
      if (!fb) return;
      const isPlay = (action === 'play');
      fb.innerHTML = `
        <div class="feedback-bubble">
          ${isPlay 
            ? '<svg width="38" height="38" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>'
            : '<svg width="38" height="38" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>'
          }
        </div>
      `;
      fb.style.display = 'flex';
      clearTimeout(fb._timeout);
      fb._timeout = setTimeout(() => {
        fb.style.display = 'none';
      }, 550);
    }

    /* VELOCIDADE DE REPRODUÇÃO */
    function cyclePlaybackSpeed() {
      const video = document.getElementById('mainVideo');
      let curr = video ? (video.playbackRate || 1.0) : 1.0;
      let idx = SPEED_OPTIONS.findIndex(s => Math.abs(s - curr) < 0.05);
      let nextIdx = (idx + 1) % SPEED_OPTIONS.length;
      setPlaybackSpeed(SPEED_OPTIONS[nextIdx]);
    }

    function adjustPlaybackSpeed(delta) {
      const video = document.getElementById('mainVideo');
      let curr = video ? (video.playbackRate || 1.0) : 1.0;
      let idx = SPEED_OPTIONS.findIndex(s => Math.abs(s - curr) < 0.05);
      if (idx === -1) idx = 1;
      let newIdx = Math.max(0, Math.min(SPEED_OPTIONS.length - 1, idx + delta));
      setPlaybackSpeed(SPEED_OPTIONS[newIdx]);
    }

    function setPlaybackSpeed(rate) {
      state.playbackSpeed = rate;
      const video = document.getElementById('mainVideo');
      if (video) video.playbackRate = rate;
      const label = document.getElementById('speedLabel');
      if (label) label.innerText = `${rate}x`;
      showToast(`Velocidade: ${rate}x`);
    }

    /* PICTURE IN PICTURE (PiP NATIVO) */
    async function togglePictureInPicture() {
      const video = document.getElementById('mainVideo');
      if (!video) return;
      try {
        if (document.pictureInPictureElement) {
          await document.exitPictureInPicture();
          showToast('PiP desativado');
        } else if (document.pictureInPictureEnabled && video.requestPictureInPicture) {
          await video.requestPictureInPicture();
          showToast('Janela Flutuante (PiP) ativada');
        } else {
          showToast('PiP não suportado neste navegador');
        }
      } catch (err) {
        console.warn('PiP error:', err);
      }
    }

    /* CONTROLE DE VOLUME & SUPER BOOSTER (ATÉ 300%) */
    let audioCtx = null;
    let gainNode = null;
    let mediaSource = null;
    let playerVolume = parseInt(localStorage.getItem('cinelocal_player_volume')) || 100;
    let previousVolume = 100;

    function initWebAudio() {
      if (audioCtx) return;
      try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        audioCtx = new AudioCtx();
        const video = document.getElementById('mainVideo');
        mediaSource = audioCtx.createMediaElementSource(video);
        gainNode = audioCtx.createGain();
        mediaSource.connect(gainNode);
        gainNode.connect(audioCtx.destination);
      } catch (e) {
        console.warn('Web Audio Booster:', e);
      }
    }

    function setPlayerVolume(val, showToastMsg = false) {
      val = Math.max(0, Math.min(300, parseInt(val) || 0));
      playerVolume = val;
      const video = document.getElementById('mainVideo');

      // Se o volume passar de 100%, inicializa a API Web Audio para amplificação por software.
      // Se for <= 100%, mantém o fluxo direto no decodificador de hardware da TV/navegador,
      // evitando qualquer buffer extra de áudio e garantindo latência zero com a legenda.
      if (val > 100) {
        initWebAudio();
        if (audioCtx && audioCtx.state === 'suspended') {
          audioCtx.resume().catch(() => {});
        }
        if (video) {
          video.volume = 1.0;
          video.muted = false;
        }
        if (gainNode) gainNode.gain.value = val / 100;
      } else {
        if (video) {
          video.volume = val / 100;
          video.muted = (val === 0);
        }
        if (gainNode) gainNode.gain.value = 1.0;
      }

      updateVolumeUI(val);
      localStorage.setItem('cinelocal_player_volume', val);
      if (showToastMsg) {
        showToast(val > 100 ? `Volume: ${val}% (BOOST 🔥)` : `Volume: ${val}%`);
      }
    }

    function updateVolumeUI(val) {
      const slider = document.getElementById('volumeSlider');
      const label = document.getElementById('volumePercent');
      const iconHigh = document.getElementById('volIconHigh');
      const iconLow = document.getElementById('volIconLow');
      const iconMuted = document.getElementById('volIconMuted');

      if (slider) {
        slider.value = val;
        slider.classList.toggle('boosted', val > 100);
      }
      if (label) {
        label.innerText = val > 100 ? `${val}% 🔥` : `${val}%`;
        label.classList.toggle('boosted', val > 100);
      }

      if (iconHigh && iconLow && iconMuted) {
        iconMuted.style.display = (val === 0) ? 'block' : 'none';
        iconLow.style.display = (val > 0 && val <= 50) ? 'block' : 'none';
        iconHigh.style.display = (val > 50) ? 'block' : 'none';
      }
    }

    function toggleMute() {
      if (playerVolume > 0) {
        previousVolume = playerVolume;
        setPlayerVolume(0, true);
      } else {
        setPlayerVolume(previousVolume > 0 ? previousVolume : 100, true);
      }
    }

    function cycleVolumeBoost() {
      const levels = [100, 150, 200, 250, 300];
      let next = levels.find(l => l > playerVolume);
      if (!next) next = 100;
      setPlayerVolume(next, true);
    }

    let lastProgressSaveTime = 0;

    function openPlayer(media, isEpisode = false, startTime = 0) {
      state.currentPlaying = media;
      state.nextEpCountdownActive = false;
      state.nextEpDismissed = false;
      clearInterval(nextEpCountdownTimer);
      const nextToast = document.getElementById('nextEpisodeToast');
      if (nextToast) nextToast.style.display = 'none';

      const video = document.getElementById('mainVideo');

      document.getElementById('playerTitle').innerText = isEpisode 
        ? `${state.currentEpisodeSeries.series.title} • ${media.title}` 
        : media.title;
      document.getElementById('playerSubInfo').innerText = `${media.resolution || '1080p'} • ${media.format || 'MKV'} ${media.isExtended ? '• Versão Estendida' : ''}`;
      
      const nextBtn = document.getElementById('btnNextEpisode');
      if (isEpisode) {
        nextBtn.style.display = 'inline-flex';
      } else {
        nextBtn.style.display = 'none';
      }

      const playerVlc = document.getElementById('playerBtnVlc');
      if (playerVlc) playerVlc.style.display = state.vlcAvailable ? 'inline-flex' : 'none';

      video.src = encodeURI(media.videoPath);
      setPlayerVolume(playerVolume, false);

      // Velocidade
      video.playbackRate = state.playbackSpeed || 1.0;
      const speedLabel = document.getElementById('speedLabel');
      if (speedLabel) speedLabel.innerText = `${state.playbackSpeed || 1.0}x`;

      // Posicionamento de retomada
      let targetTime = startTime;
      if (targetTime === 0) {
        const prog = getWatchProgress(media.id);
        if (prog && prog.currentTime > 15 && !prog.completed) {
          targetTime = prog.currentTime;
          showToast(`Retomando de ${formatTime(targetTime)}...`);
        }
      }

      video.onloadedmetadata = () => {
        if (targetTime > 0 && video.duration && targetTime < video.duration) {
          video.currentTime = targetTime;
        }
        video.play().catch(() => {});
      };

      // Legendas
      state.subtitleCues = [];
      const subList = document.getElementById('subtitlesList');
      subList.innerHTML = '';

      if (media.subtitles && media.subtitles.length > 0) {
        media.subtitles.forEach((s) => {
          const btn = document.createElement('button');
          btn.className = 'dropdown-item';
          btn.innerText = s.label;
          btn.dataset.path = s.path;
          btn.onclick = () => selectSubtitle(s.path, true);
          subList.appendChild(btn);
        });

        // Adiciona opção Desligada
        const offBtn = document.createElement('button');
        offBtn.className = 'dropdown-item';
        offBtn.innerText = 'Desativada';
        offBtn.onclick = () => disableSubtitles(true);
        subList.appendChild(offBtn);

        // Se houver legenda em português, ativa automaticamente
        const ptSub = media.subtitles.find(s => s.label.toLowerCase().includes('portugu') && !s.label.toLowerCase().includes('forçada')) || media.subtitles[0];
        if (ptSub) {
          selectSubtitle(ptSub.path, false);
        } else {
          disableSubtitles(false);
        }
      } else {
        subList.innerHTML = '<div style="font-size: 12px; color: var(--text-muted); padding: 4px 8px;">Sem legendas externas</div>';
        disableSubtitles(false);
      }

      // Faixas de Áudio
      const audioList = document.getElementById('audioTracksList');
      if (audioList) {
        audioList.innerHTML = '<div style="font-size: 12px; color: var(--text-muted); padding: 4px 8px;">Detectando áudios...</div>';
        if (window.location.protocol.startsWith('http')) {
          fetch(`/api/audio_info?path=${encodeURIComponent(media.videoPath)}`)
            .then(r => r.ok ? r.json() : Promise.reject())
            .then(data => {
              if (data.streams && data.streams.length > 0) {
                audioList.innerHTML = '';
                data.streams.forEach(st => {
                  const btn = document.createElement('button');
                  btn.className = 'dropdown-item' + (st.index === 1 ? ' active' : '');
                  btn.innerText = st.label;
                  btn.onclick = () => selectAudioTrack(media, st.index);
                  audioList.appendChild(btn);
                });
              } else {
                audioList.innerHTML = '<div style="font-size: 12px; color: var(--text-muted); padding: 4px 8px;">Áudio Padrão (Nativo)</div>';
              }
            })
            .catch(() => {
              audioList.innerHTML = '<div style="font-size: 12px; color: var(--text-muted); padding: 4px 8px;">Áudio Padrão (Nativo)</div>';
            });
        } else {
          audioList.innerHTML = '<div style="font-size: 12px; color: var(--text-muted); padding: 4px 8px;">Áudio Padrão (Nativo)</div>';
        }
      }

      updateSubSyncUI();
      document.getElementById('playerModal').classList.add('active');
      document.body.style.overflow = 'hidden';

      resetControlsTimer();
    }

    function selectAudioTrack(media, audioIndex) {
      const video = document.getElementById('mainVideo');
      if (!video) return;
      const curr = video.currentTime;
      video.pause();
      video.src = `/api/stream?path=${encodeURIComponent(media.videoPath)}&audio=${audioIndex}&ss=${Math.floor(curr)}`;
      video.load();
      video.play().catch(() => {});
      document.querySelectorAll('#audioTracksList .dropdown-item').forEach((btn, idx) => {
        btn.classList.toggle('active', idx === (audioIndex - 1));
      });
      toggleDropdown('audioMenu');
      showToast('Faixa de áudio alterada');
    }

    function closePlayer() {
      const video = document.getElementById('mainVideo');
      if (video) {
        if (state.currentPlaying && video.duration) {
          saveWatchProgress(state.currentPlaying.id, video.currentTime, video.duration, state.currentPlaying);
        }
        video.pause();
        video.removeAttribute('src');
        video.load();
      }

      clearInterval(nextEpCountdownTimer);
      state.nextEpCountdownActive = false;

      document.getElementById('playerModal').classList.remove('active');
      document.body.style.overflow = '';
      state.currentPlaying = null;

      renderHomeCarousels();
      renderMoviesGrid();
    }

    function togglePlayPause() {
      const video = document.getElementById('mainVideo');
      if (!video) return;
      if (video.paused) {
        video.play().catch(() => {});
      } else {
        video.pause();
      }
    }

    function skipTime(seconds) {
      const video = document.getElementById('mainVideo');
      if (!video) return;
      video.currentTime = Math.max(0, Math.min(video.duration || 0, video.currentTime + seconds));
      showToast(`${seconds > 0 ? '+' : ''}${seconds}s`);
    }

    function toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.getElementById('playerModal').requestFullscreen().catch(() => {});
      } else {
        document.exitFullscreen().catch(() => {});
      }
    }

    function handleSeekClick(e) {
      const bar = document.getElementById('seekBarContainer');
      const rect = bar.getBoundingClientRect();
      const pos = (e.clientX - rect.left) / rect.width;
      const video = document.getElementById('mainVideo');
      if (video.duration) {
        video.currentTime = pos * video.duration;
      }
    }

    function setupSeekDrag() {
      const video = document.getElementById('mainVideo');
      if (!video) return;

      video.addEventListener('timeupdate', () => {
        if (!video.duration) return;
        const pct = (video.currentTime / video.duration) * 100;
        const fillEl = document.getElementById('seekFill');
        if (fillEl) fillEl.style.width = pct + '%';
        const timeEl = document.getElementById('timeDisplay');
        if (timeEl) timeEl.innerText = `${formatTime(video.currentTime)} / ${formatTime(video.duration)}`;
        renderSubtitles(video.currentTime);

        // Salvar progresso a cada 4 segundos
        const now = Date.now();
        if (state.currentPlaying && now - lastProgressSaveTime > 4000) {
          lastProgressSaveTime = now;
          saveWatchProgress(state.currentPlaying.id, video.currentTime, video.duration, state.currentPlaying);
        }

        // Alerta de próximo episódio nos últimos 20 segundos
        if (state.currentEpisodeSeries && video.duration > 35) {
          const remaining = video.duration - video.currentTime;
          if (remaining <= 20 && remaining > 1 && !state.nextEpCountdownActive && !state.nextEpDismissed) {
            startNextEpisodeCountdown(Math.floor(remaining));
          }
        }
      });

      video.addEventListener('progress', () => {
        if (video.buffered.length > 0 && video.duration) {
          const buf = (video.buffered.end(video.buffered.length - 1) / video.duration) * 100;
          const bufEl = document.getElementById('seekBuffered');
          if (bufEl) bufEl.style.width = buf + '%';
        }
      });

      video.addEventListener('ended', () => {
        if (state.currentPlaying && video.duration) {
          saveWatchProgress(state.currentPlaying.id, video.duration, video.duration, state.currentPlaying);
        }
        if (state.currentEpisodeSeries) {
          playNextEpisodeImmediately();
        }
      });
    }

    function setupPlayerEvents() {
      const video = document.getElementById('mainVideo');
      if (!video) return;

      video.addEventListener('play', () => {
        const playIcon = document.getElementById('playIcon');
        const pauseIcon = document.getElementById('pauseIcon');
        if (playIcon) playIcon.style.display = 'none';
        if (pauseIcon) pauseIcon.style.display = 'block';
        showCenterPulse('play');
        resetControlsTimer();
      });

      video.addEventListener('pause', () => {
        const playIcon = document.getElementById('playIcon');
        const pauseIcon = document.getElementById('pauseIcon');
        if (playIcon) playIcon.style.display = 'block';
        if (pauseIcon) pauseIcon.style.display = 'none';
        showCenterPulse('pause');
        resetControlsTimer();
      });

      document.addEventListener('mousemove', () => {
        const modal = document.getElementById('playerModal');
        if (modal && modal.classList.contains('active')) {
          resetControlsTimer();
        }
      });

      document.addEventListener('fullscreenchange', () => {
        resetControlsTimer();
      });
    }

    function formatTime(s) {
      const hrs = Math.floor(s / 3600);
      const mins = Math.floor((s % 3600) / 60);
      const secs = Math.floor(s % 60);
      if (hrs > 0) {
        return `${hrs}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
      }
      return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }

    /* LEGENDAS */
    function parseClientSRT(content) {
      if (!content) return [];
      const blocks = content.trim().split(/\r?\n\r?\n+/);
      const cues = [];
      for (const b of blocks) {
        const lines = b.trim().split('\n');
        if (lines.length < 2) continue;
        const idx = /^\d+$/.test(lines[0].trim()) ? 1 : 0;
        if (idx >= lines.length || !lines[idx].includes('-->')) continue;
        const m = lines[idx].match(/(\d{1,2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{1,2}):(\d{2}):(\d{2})[,.](\d{3})/);
        if (!m) continue;
        const s = parseInt(m[1])*3600 + parseInt(m[2])*60 + parseInt(m[3]) + parseInt(m[4])/1000;
        const e = parseInt(m[5])*3600 + parseInt(m[6])*60 + parseInt(m[7]) + parseInt(m[8])/1000;
        let txt = lines.slice(idx + 1).join('\n').trim();
        txt = txt.replace(/\{[^}]+\}/g, '').replace(/<\/?font[^>]*>/gi, '').trim();
        if (txt) cues.push([Math.round(s * 100) / 100, Math.round(e * 100) / 100, txt]);
      }
      return cues;
    }

    function selectSubtitle(subPath, fromUserClick = false) {
      state.activeSubtitle = subPath;
      let cues = null;

      if (window.LEGENDAS_DB) {
        if (window.LEGENDAS_DB[subPath]) {
          cues = window.LEGENDAS_DB[subPath];
        } else {
          const norm = subPath.replace(/\\/g, '/').toLowerCase();
          const fname = subPath.split('/').pop().toLowerCase();
          for (const key of Object.keys(window.LEGENDAS_DB)) {
            const knorm = key.replace(/\\/g, '/').toLowerCase();
            if (knorm === norm || knorm.endsWith(fname)) {
              cues = window.LEGENDAS_DB[key];
              break;
            }
          }
        }
      }

      if (cues && cues.length > 0) {
        state.subtitleCues = cues;
        if (fromUserClick) showToast('Legenda ativada');
      } else {
        // Tenta buscar o arquivo .srt diretamente se não estiver no banco
        fetch(encodeURI(subPath))
          .then(res => res.ok ? res.text() : Promise.reject())
          .then(text => {
            const parsed = parseClientSRT(text);
            if (parsed.length > 0) {
              state.subtitleCues = parsed;
              if (fromUserClick) showToast('Legenda carregada');
            }
          })
          .catch(() => {});
      }

      document.querySelectorAll('#subtitlesList .dropdown-item').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.path === subPath);
      });

      if (fromUserClick) {
        toggleDropdown('subtitlesMenu');
      }
    }

    function disableSubtitles(fromUserClick = false) {
      state.activeSubtitle = null;
      state.subtitleCues = [];
      const textEl = document.getElementById('subtitleText');
      if (textEl) {
        textEl.style.display = 'none';
        textEl.dataset.currentCue = '';
        textEl.innerHTML = '';
      }
      document.querySelectorAll('#subtitlesList .dropdown-item').forEach(btn => {
        btn.classList.toggle('active', !btn.dataset.path);
      });
      if (fromUserClick) {
        toggleDropdown('subtitlesMenu');
        showToast('Legenda desativada');
      }
    }

    function setSubSize(sz) {
      state.subSize = sz;
      const el = document.getElementById('subtitleDisplay');
      if (el) el.className = `subtitle-display size-${sz}`;
    }

    function updateSubSyncUI() {
      const lbl = document.getElementById('subSyncValueLabel');
      if (lbl) {
        const sign = state.subSyncOffset > 0 ? '+' : '';
        lbl.innerText = `${sign}${state.subSyncOffset.toFixed(1)}s`;
      }
    }

    function adjustSubSync(delta) {
      state.subSyncOffset = Math.round((state.subSyncOffset + delta) * 10) / 10;
      localStorage.setItem('cinelocal_sub_sync_offset', state.subSyncOffset);
      updateSubSyncUI();
      const sign = state.subSyncOffset > 0 ? '+' : '';
      showToast(`Sincronia da legenda: ${sign}${state.subSyncOffset.toFixed(1)}s`);
    }

    function resetSubSync() {
      state.subSyncOffset = 0.0;
      localStorage.setItem('cinelocal_sub_sync_offset', 0.0);
      updateSubSyncUI();
      showToast('Sincronia da legenda redefinida (0.0s)');
    }

    function renderSubtitles(currTime) {
      const textEl = document.getElementById('subtitleText');
      if (!textEl || !state.subtitleCues || state.subtitleCues.length === 0) {
        if (textEl && textEl.style.display !== 'none') {
          textEl.style.display = 'none';
          textEl.dataset.currentCue = '';
        }
        return;
      }
      const adjusted = currTime + state.subSyncOffset;
      const cue = state.subtitleCues.find(c => adjusted >= c[0] && adjusted <= c[1]);
      if (cue) {
        if (textEl.dataset.currentCue !== cue[2]) {
          textEl.dataset.currentCue = cue[2];
          textEl.innerHTML = cue[2].replace(/\n/g, '<br>');
        }
        textEl.style.display = 'inline-block';
      } else {
        if (textEl.style.display !== 'none') {
          textEl.style.display = 'none';
          textEl.dataset.currentCue = '';
        }
      }
    }

    function toggleDropdown(menuId) {
      const m = document.getElementById(menuId);
      m.classList.toggle('active');
    }

    function handleViewportClick(e) {
      if (e.target.closest('#nextEpisodeToast') || e.target.closest('.player-bottom-controls') || e.target.closest('.player-top-bar')) {
        return;
      }
      togglePlayPause();
      resetControlsTimer();
    }

    function resetControlsTimer() {
      clearTimeout(state.controlsTimeout);
      const container = document.getElementById('playerContainer');
      if (!container) return;
      container.classList.remove('controls-hidden');
      const video = document.getElementById('mainVideo');
      if (video && !video.paused) {
        state.controlsTimeout = setTimeout(() => {
          if (!document.querySelector('.dropdown-menu.active')) {
            container.classList.add('controls-hidden');
          }
        }, 3500);
      }
    }

    /* VLC INTEGRATION */
    function launchVlc(videoPath) {
      if (state.vlcAvailable === false) {
        showToast('VLC não detectado. Reproduzindo no player web nativo.');
        return;
      }
      showToast('Iniciando VLC (Áudio 5.1)...');
      fetch(`/api/open_vlc?path=${encodeURIComponent(videoPath)}`)
        .then(r => r.json())
        .then(data => {
          if (data.status === 'ok') {
            showToast('Vídeo aberto com sucesso no VLC!');
          } else {
            showToast('Aviso: ' + (data.message || 'Erro ao abrir VLC'));
          }
        })
        .catch(() => {
          showToast('Servidor offline para VLC');
        });
    }

    function launchCurrentInVlc() {
      if (state.vlcAvailable === false) {
        showToast('VLC não detectado. Reproduzindo no player web nativo.');
        return;
      }
      if (state.currentPlaying) {
        const video = document.getElementById('mainVideo');
        if (video) {
          video.pause();
          const pIcon = document.getElementById('playIcon');
          const paIcon = document.getElementById('pauseIcon');
          if (pIcon) pIcon.style.display = 'block';
          if (paIcon) paIcon.style.display = 'none';
        }
        showToast('Pausando player e abrindo no VLC...');
        launchVlc(state.currentPlaying.videoPath);
      }
    }

    /* BUSCA INSTANTÂNEA GLOBAL */
    function handleSearchInput(query) {
      state.searchQuery = query.trim();
      document.getElementById('searchClearBtn').style.display = state.searchQuery ? 'block' : 'none';

      if (state.searchQuery.length > 0) {
        if (state.activeView === 'home') {
          switchView('movies');
        }
        renderMoviesGrid();
      } else {
        renderMoviesGrid();
      }
    }

    function clearSearch() {
      document.getElementById('globalSearchInput').value = '';
      handleSearchInput('');
    }

    /* MODAL SURPREENDA-ME (ROLETA DE FILMES) */
    function openSurpriseModal() {
      if (!state.movies || state.movies.length === 0) {
        showToast('Nenhum filme carregado no catálogo.');
        return;
      }
      spinSurpriseMovie();
      document.getElementById('surpriseModal').classList.add('active');
      document.body.style.overflow = 'hidden';
    }

    function closeSurpriseModal() {
      const modal = document.getElementById('surpriseModal');
      if (modal) modal.classList.remove('active');
      document.body.style.overflow = '';
    }

    function closeSurpriseModalOnOut(e) {
      if (e.target.id === 'surpriseModal') closeSurpriseModal();
    }

    function spinSurpriseMovie() {
      if (!state.movies || state.movies.length === 0) return;
      const randIdx = Math.floor(Math.random() * state.movies.length);
      const mov = state.movies[randIdx];
      state.currentSurpriseMovie = mov;

      const cardBox = document.getElementById('surpriseCardBox');
      if (cardBox) {
        cardBox.style.opacity = '0';
        setTimeout(() => {
          const postEl = document.getElementById('surprisePoster');
          if (postEl) postEl.src = mov.posterPath ? encodeURI(mov.posterPath) : '';
          const titEl = document.getElementById('surpriseTitle');
          if (titEl) titEl.innerText = mov.title;
          const yrEl = document.getElementById('surpriseYear');
          if (yrEl) yrEl.innerText = mov.year || '';
          const resEl = document.getElementById('surpriseRes');
          if (resEl) resEl.innerText = mov.resolution || '1080p';
          const ratEl = document.getElementById('surpriseRating');
          if (ratEl) ratEl.innerText = mov.rating ? `⭐ ${mov.rating}` : '⭐ 7.5';
          const ovEl = document.getElementById('surpriseOverview');
          if (ovEl) ovEl.innerText = mov.overview || 'Uma excelente escolha do catálogo do CineLocal para você curtir agora.';

          const playBtn = document.getElementById('btnSurprisePlay');
          if (playBtn) {
            playBtn.onclick = () => {
              closeSurpriseModal();
              openPlayer(mov);
            };
          }
          cardBox.style.opacity = '1';
        }, 120);
      }
    }

    /* MODAL CONECTAR SMART TV OU CONTROLE REMOTO (QR CODE) */
    function openQrConnectModal(initialTab = 'tv') {
      const modal = document.getElementById('qrModal');
      if (!modal) return;
      switchQrTab(initialTab);
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
    }

    function switchQrTab(tabName) {
      const isRemote = (tabName === 'remote');
      const baseIpUrl = state.localUrl || `http://${window.location.hostname || 'localhost'}:8000/`;
      const targetUrl = isRemote ? `${baseIpUrl.replace(/\/$/, '')}/remote` : baseIpUrl;

      const tabTv = document.getElementById('qrTabTv');
      const tabRemote = document.getElementById('qrTabRemote');
      if (tabTv) tabTv.classList.toggle('active', !isRemote);
      if (tabRemote) tabRemote.classList.toggle('active', isRemote);

      const titleEl = document.getElementById('qrModalTitle');
      if (titleEl) {
        titleEl.innerText = isRemote ? '📱 Controle Remoto Virtual' : '📺 Conectar Smart TV ou Celular';
      }

      const descEl = document.getElementById('qrModalDesc');
      if (descEl) {
        descEl.innerText = isRemote 
          ? 'Abra a câmera do seu celular para comandar a Smart TV sem mouse nem teclado:'
          : 'Conecte seu dispositivo na mesma rede Wi-Fi e aponte a câmera para abrir o CineLocal:';
      }

      const urlEl = document.getElementById('qrLocalUrlDisplay');
      if (urlEl) urlEl.innerText = targetUrl;

      const qrWrapper = document.getElementById('qrSvgWrapper');
      if (qrWrapper) {
        const qrApiUrl = `https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=${encodeURIComponent(targetUrl)}&bgcolor=13-17-22&color=ffffff&margin=10`;
        qrWrapper.innerHTML = `
          <img src="${qrApiUrl}" alt="QR Code CineLocal" style="width: 220px; height: 220px; border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.6);" onerror="this.onerror=null; this.parentElement.innerHTML='<div style=\\'padding: 24px; color: var(--text-muted); font-size: 0.9rem; text-align: center;\\'>📡 Acesse este endereço no celular: <br><strong>${targetUrl}</strong></div>';">
        `;
      }
    }

    function closeQrModal() {
      const modal = document.getElementById('qrModal');
      if (modal) modal.classList.remove('active');
      document.body.style.overflow = '';
    }

    function closeQrModalOnOut(e) {
      if (e.target.id === 'qrModal') closeQrModal();
    }

    /* RECEPTOR DO CONTROLE REMOTO VIRTUAL (SMART TV / PC) */
    function setupRemoteControlListener() {
      if (!window.location.protocol.startsWith('http')) return;

      function executeRemoteCommand(action, payload) {
        const isPlayerOpen = document.getElementById('playerModal') && document.getElementById('playerModal').classList.contains('active');

        switch(action) {
          case 'up':
            if (isPlayerOpen) {
              setPlayerVolume(playerVolume + 5, true);
            } else {
              handleDpadNavigation('ArrowUp');
            }
            break;
          case 'down':
            if (isPlayerOpen) {
              setPlayerVolume(playerVolume - 5, true);
            } else {
              handleDpadNavigation('ArrowDown');
            }
            break;
          case 'left':
            if (isPlayerOpen) {
              skipTime(-10);
            } else {
              handleDpadNavigation('ArrowLeft');
            }
            break;
          case 'right':
            if (isPlayerOpen) {
              skipTime(10);
            } else {
              handleDpadNavigation('ArrowRight');
            }
            break;
          case 'enter':
            if (isPlayerOpen) {
              togglePlayPause();
            } else {
              if (document.activeElement && typeof document.activeElement.click === 'function') {
                document.activeElement.click();
              }
            }
            break;
          case 'play_pause':
            togglePlayPause();
            break;
          case 'skip_fwd':
            skipTime(10);
            break;
          case 'skip_bwd':
            skipTime(-10);
            break;
          case 'vol_up':
            setPlayerVolume(playerVolume + 5, true);
            break;
          case 'vol_down':
            setPlayerVolume(playerVolume - 5, true);
            break;
          case 'mute':
            toggleMute();
            break;
          case 'fullscreen':
            toggleFullscreen();
            break;
          case 'sub_sync_minus':
            adjustSubSync(-0.1);
            break;
          case 'sub_sync_plus':
            adjustSubSync(0.1);
            break;
          case 'sub_toggle':
            if (state.activeSubtitle) {
              disableSubtitles(true);
            } else if (state.currentPlaying && state.currentPlaying.subtitles && state.currentPlaying.subtitles.length > 0) {
              selectSubtitle(state.currentPlaying.subtitles[0].path, true);
            }
            break;
          case 'back':
            if (isPlayerOpen) {
              closePlayer();
            } else {
              closeMovieModal();
              closeSeriesModal();
              closeSurpriseModal();
              closeTrailerModal();
              closeQrModal();
            }
            break;
        }
      }

      let sseActive = false;
      try {
        const evtSource = new EventSource('/api/remote/events');
        evtSource.onopen = () => {
          sseActive = true;
        };
        evtSource.onmessage = (e) => {
          try {
            const data = JSON.parse(e.data);
            if (data && data.action) {
              executeRemoteCommand(data.action, data.payload);
            }
          } catch (err) {}
        };
        evtSource.onerror = () => {
          if (!sseActive) {
            startPollingFallback(executeRemoteCommand);
          }
        };
      } catch (e) {
        startPollingFallback(executeRemoteCommand);
      }
    }

    let lastPolledRemoteId = 0;
    function startPollingFallback(callback) {
      setInterval(async () => {
        try {
          const res = await fetch(`/api/remote/poll?since=${lastPolledRemoteId}`);
          if (res.ok) {
            const data = await res.json();
            if (data.events && data.events.length > 0) {
              data.events.forEach(ev => {
                if (ev.id > lastPolledRemoteId) {
                  lastPolledRemoteId = ev.id;
                  callback(ev.action, ev.payload);
                }
              });
            }
          }
        } catch (e) {}
      }, 500);
    }

    /* NAVEGAÇÃO D-PAD PARA SMART TV E CONTROLE REMOTO */
    function handleDpadNavigation(key) {
      const isAnyModalOpen = document.querySelector('.series-modal.active, .player-modal.active');
      if (isAnyModalOpen) return;

      const focusables = Array.from(document.querySelectorAll('.movie-card, .nav-btn, .chip, .btn-header-action'));
      if (focusables.length === 0) return;

      const active = document.activeElement;
      let currentIndex = focusables.indexOf(active);

      if (currentIndex === -1) {
        focusables[0].focus();
        return;
      }

      const currentRect = active.getBoundingClientRect();
      let bestNext = null;
      let bestDist = Infinity;

      focusables.forEach((el, idx) => {
        if (idx === currentIndex) return;
        const r = el.getBoundingClientRect();
        if (r.width === 0 || r.height === 0) return;

        let isCandidate = false;
        let dist = 0;
        if (key === 'ArrowRight' && r.left >= currentRect.right - 10) {
          isCandidate = true;
          dist = Math.hypot(r.left - currentRect.right, (r.top - currentRect.top) * 0.7);
        } else if (key === 'ArrowLeft' && r.right <= currentRect.left + 10) {
          isCandidate = true;
          dist = Math.hypot(currentRect.left - r.right, (r.top - currentRect.top) * 0.7);
        } else if (key === 'ArrowDown' && r.top >= currentRect.bottom - 10) {
          isCandidate = true;
          dist = Math.hypot(r.left - currentRect.left, (r.top - currentRect.bottom) * 1.5);
        } else if (key === 'ArrowUp' && r.bottom <= currentRect.top + 10) {
          isCandidate = true;
          dist = Math.hypot(r.left - currentRect.left, (currentRect.top - r.bottom) * 1.5);
        }

        if (isCandidate && dist < bestDist) {
          bestDist = dist;
          bestNext = el;
        }
      });

      if (bestNext) {
        bestNext.focus();
        bestNext.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'nearest' });
      } else {
        if (key === 'ArrowRight' || key === 'ArrowDown') {
          const nextIdx = (currentIndex + 1) % focusables.length;
          focusables[nextIdx].focus();
          focusables[nextIdx].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'nearest' });
        } else if (key === 'ArrowLeft' || key === 'ArrowUp') {
          const prevIdx = (currentIndex - 1 + focusables.length) % focusables.length;
          focusables[prevIdx].focus();
          focusables[prevIdx].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'nearest' });
        }
      }
    }

    /* ATALHOS DE TECLADO */
    function setupKeyboardShortcuts() {
      window.addEventListener('keydown', e => {
        if (e.target.tagName === 'INPUT') return;

        const isPlayerOpen = document.getElementById('playerModal').classList.contains('active');

        if (e.key === 'Escape') {
          if (isPlayerOpen) closePlayer();
          closeSeriesModal();
          closeMovieModal();
          closeMcuTrackerModal();
          closeSurpriseModal();
          closeTrailerModal();
          closeQrModal();
        }

        if (isPlayerOpen) {
          if (e.key === ' ' || e.key.toLowerCase() === 'k') {
            e.preventDefault();
            togglePlayPause();
          } else if (e.key === 'ArrowRight') {
            e.preventDefault();
            skipTime(10);
          } else if (e.key === 'ArrowLeft') {
            e.preventDefault();
            skipTime(-10);
          } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            setPlayerVolume(playerVolume + 5, true);
          } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            setPlayerVolume(playerVolume - 5, true);
          } else if (e.key.toLowerCase() === 'm') {
            e.preventDefault();
            toggleMute();
          } else if (e.key.toLowerCase() === 'f') {
            e.preventDefault();
            toggleFullscreen();
          } else if (e.key.toLowerCase() === 'v') {
            e.preventDefault();
            launchCurrentInVlc();
          } else if (e.key.toLowerCase() === 'n') {
            e.preventDefault();
            playNextEpisode();
          } else if (e.key.toLowerCase() === 'p') {
            e.preventDefault();
            togglePictureInPicture();
          } else if (e.key === '[') {
            e.preventDefault();
            adjustPlaybackSpeed(-1);
          } else if (e.key === ']') {
            e.preventDefault();
            adjustPlaybackSpeed(1);
          } else if (e.key.toLowerCase() === 'c') {
            e.preventDefault();
            toggleDropdown('subtitlesMenu');
          } else if (e.key.toLowerCase() === 'g') {
            e.preventDefault();
            adjustSubSync(-0.1);
          } else if (e.key.toLowerCase() === 'h') {
            e.preventDefault();
            adjustSubSync(0.1);
          }
        } else {
          // Fora do player: Atalho / para Busca, Smart TV D-Pad e Enter
          if (e.key === '/') {
            e.preventDefault();
            const searchInput = document.getElementById('globalSearchInput');
            if (searchInput) {
              searchInput.focus();
              searchInput.select();
            }
          } else if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(e.key)) {
            e.preventDefault();
            handleDpadNavigation(e.key);
          } else if (e.key === 'Enter') {
            if (document.activeElement && document.activeElement.classList.contains('movie-card')) {
              e.preventDefault();
              document.activeElement.click();
            }
          }
        }
      });
    }

    function showToast(msg) {
      const container = document.getElementById('toastContainer');
      const toast = document.createElement('div');
      toast.className = 'toast';
      toast.innerText = msg;
      container.appendChild(toast);
      setTimeout(() => {
        toast.remove();
      }, 3000);
    }

    function showHelpModal() {
      alert("CineLocal Home Theater:\n\n• Início: Destaques, Continuar Assistindo, carrosséis e MCU.\n• Filmes: Grade completa com filtros por gênero, ano e status.\n• Séries: The Bear e temporadas completas.\n• Player: Espaço (Play/Pause), Setas (Pular 10s e Volume), F (Fullscreen), P (PiP), [ e ] (Velocidade), V (VLC).\n• Smart TV: Navegue facilmente com as setas do controle remoto e OK/Enter.");
    }
  </script>
</body>
</html>
"""

def generate():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"CineLocal UI gerada com sucesso em: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate()
