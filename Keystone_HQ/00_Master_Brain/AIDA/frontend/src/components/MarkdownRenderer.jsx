import React from 'react';
import { FileText } from 'lucide-react';

const copyToClipboard = (text) => {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).catch(err => {
      fallbackCopy(text);
    });
  } else {
    fallbackCopy(text);
  }
};

const fallbackCopy = (text) => {
  const textArea = document.createElement("textarea");
  textArea.value = text;
  textArea.style.top = "0";
  textArea.style.left = "0";
  textArea.style.position = "fixed";
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  try {
    document.execCommand('copy');
  } catch (err) {
    console.error('Fallback copy failed', err);
  }
  document.body.removeChild(textArea);
};

// Simple inline parser for bold, code spans, links, files, and specific components
const parseInline = (text, onLinkClick) => {
  if (!text) return '';
  
  // Match:
  // 1. inline code: `code`
  // 2. bold text: **bold**
  // 3. markdown links: [text](href)
  // 4. file names/paths: ending with .jsx, .py, .json, .js, .css, .md, .txt
  // 5. specific system terms: ArchivePanel, ChatArea, Sidebar, VoiceOrb, Chronos, Recomposition, Protocols, Possibilities, Webmaster
  const tokenRegex = /(`[^`]+`|\*\*[^*]+\*\*|\[[^\]]+\]\([^)]+\)|\b[\w\-_\/]+\.(?:jsx|py|json|js|css|md|txt)\b|\b(?:ArchivePanel|ChatArea|Sidebar|VoiceOrb|Chronos|Recomposition|Protocols|Possibilities|Webmaster)\b)/g;
  
  const parts = text.split(tokenRegex);
  return parts.map((part, index) => {
    if (!part) return null;
    
    if (part.startsWith('`') && part.endsWith('`')) {
      const innerText = part.slice(1, -1);
      if (/\b[\w\-_\/]+\.(?:jsx|py|json|js|css|md|txt)\b/.test(innerText)) {
        const pathMap = {
          'App.jsx': 'c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/AIDA_V2/frontend/src/App.jsx',
          'ChatArea.jsx': 'c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/AIDA_V2/frontend/src/components/ChatArea.jsx',
          'Sidebar.jsx': 'c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/AIDA_V2/frontend/src/components/Sidebar.jsx',
          'ArchivePanel.jsx': 'c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/AIDA_V2/frontend/src/components/ArchivePanel.jsx',
          'VoiceOrb.jsx': 'c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/AIDA_V2/frontend/src/components/VoiceOrb.jsx',
          'Footer.jsx': 'c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/AIDA_V2/frontend/src/components/Footer.jsx',
          'server.py': 'c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/AIDA_V2/backend/server.py',
          'chat_manager.py': 'c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/AIDA_V2/backend/chat_manager.py',
          'implementation_plan.md': 'c:/Users/Curtis/.gemini/antigravity/brain/f5802ba0-efbe-43c0-8a75-0dae6ef9d9c8/implementation_plan.md',
          'system_status.py': 'c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/scripts/system_status.py',
          'obsidian_audit.py': 'c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/scripts/obsidian_audit.py'
        };
        
        let mappedPath = pathMap[innerText] || innerText;
        if (!mappedPath.startsWith('c:/') && !mappedPath.startsWith('C:/') && !mappedPath.startsWith('file://')) {
          mappedPath = 'c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/' + mappedPath;
        }
        
        return (
          <span 
            key={index}
            onClick={() => {
              if (onLinkClick) {
                onLinkClick(mappedPath, innerText);
              }
            }}
            className="file-badge"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '4px',
              backgroundColor: 'rgba(0, 212, 255, 0.05)',
              border: '1px solid rgba(0, 212, 255, 0.25)',
              color: 'var(--accent-blue)',
              padding: '2px 6px',
              borderRadius: '4px',
              fontSize: '11px',
              fontFamily: 'monospace',
              cursor: 'pointer',
              verticalAlign: 'middle',
              margin: '0 2px',
              transition: 'all 0.2s ease'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = 'var(--accent-blue)';
              e.currentTarget.style.backgroundColor = 'rgba(0, 212, 255, 0.15)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = 'rgba(0, 212, 255, 0.25)';
              e.currentTarget.style.backgroundColor = 'rgba(0, 212, 255, 0.05)';
            }}
          >
            <FileText size={11} color="var(--accent-blue)" />
            {innerText}
          </span>
        );
      }
      return (
        <code key={index} style={{
          backgroundColor: 'rgba(0,0,0,0.3)',
          padding: '2px 5px',
          borderRadius: '3px',
          fontFamily: 'monospace',
          fontSize: '12px',
          color: '#e2f0fe',
          border: '1px solid rgba(255,255,255,0.05)'
        }}>
          {innerText}
        </code>
      );
    }
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={index} style={{ color: 'var(--text-main)' }}>{part.slice(2, -2)}</strong>;
    }
    if (part.startsWith('[') && part.includes('](') && part.endsWith(')')) {
      const match = part.match(/\[([^\]]+)\]\(([^)]+)\)/);
      if (match) {
        const linkText = match[1];
        const href = match[2];
        const isFileUrl = href.startsWith('file://');
        
        return (
          <a 
            key={index} 
            href={href}
            onClick={(e) => {
              if (isFileUrl || href.startsWith('/') || href.includes(':')) {
                e.preventDefault();
                if (onLinkClick) {
                  onLinkClick(href, linkText);
                }
              }
            }}
            style={{
              color: 'var(--accent-blue)',
              textDecoration: 'underline',
              cursor: 'pointer',
              fontWeight: 500
            }}
          >
            {linkText}
          </a>
        );
      }
    }
    
    // Check if it is a file match
    if (/\b[\w\-_\/]+\.(?:jsx|py|json|js|css|md|txt)\b/.test(part)) {
      const pathMap = {
        'App.jsx': 'c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/AIDA_V2/frontend/src/App.jsx',
        'ChatArea.jsx': 'c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/AIDA_V2/frontend/src/components/ChatArea.jsx',
        'Sidebar.jsx': 'c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/AIDA_V2/frontend/src/components/Sidebar.jsx',
        'ArchivePanel.jsx': 'c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/AIDA_V2/frontend/src/components/ArchivePanel.jsx',
        'VoiceOrb.jsx': 'c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/AIDA_V2/frontend/src/components/VoiceOrb.jsx',
        'Footer.jsx': 'c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/AIDA_V2/frontend/src/components/Footer.jsx',
        'server.py': 'c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/AIDA_V2/backend/server.py',
        'chat_manager.py': 'c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/AIDA_V2/backend/chat_manager.py',
        'implementation_plan.md': 'c:/Users/Curtis/.gemini/antigravity/brain/f5802ba0-efbe-43c0-8a75-0dae6ef9d9c8/implementation_plan.md',
        'system_status.py': 'c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/scripts/system_status.py',
        'obsidian_audit.py': 'c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/scripts/obsidian_audit.py'
      };
      
      let mappedPath = pathMap[part] || part;
      if (!mappedPath.startsWith('c:/') && !mappedPath.startsWith('C:/') && !mappedPath.startsWith('file://')) {
        mappedPath = 'c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/' + mappedPath;
      }
      return (
        <span 
          key={index}
          onClick={() => {
            if (onLinkClick) {
              onLinkClick(mappedPath, part);
            }
          }}
          className="file-badge"
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '4px',
            backgroundColor: 'rgba(0, 212, 255, 0.05)',
            border: '1px solid rgba(0, 212, 255, 0.25)',
            color: 'var(--accent-blue)',
            padding: '2px 6px',
            borderRadius: '4px',
            fontSize: '11px',
            fontFamily: 'monospace',
            cursor: 'pointer',
            verticalAlign: 'middle',
            margin: '0 2px',
            transition: 'all 0.2s ease'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.borderColor = 'var(--accent-blue)';
            e.currentTarget.style.backgroundColor = 'rgba(0, 212, 255, 0.15)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.borderColor = 'rgba(0, 212, 255, 0.25)';
            e.currentTarget.style.backgroundColor = 'rgba(0, 212, 255, 0.05)';
          }}
        >
          <FileText size={11} color="var(--accent-blue)" />
          {part}
        </span>
      );
    }
    
    // Check if it is a specific system term match
    if (/\b(?:ArchivePanel|ChatArea|Sidebar|VoiceOrb|Chronos|Recomposition|Protocols|Possibilities|Webmaster)\b/.test(part)) {
      return (
        <span 
          key={index}
          style={{
            backgroundColor: 'rgba(0, 212, 255, 0.08)',
            border: '1px solid rgba(0, 212, 255, 0.25)',
            color: 'var(--accent-blue)',
            padding: '2px 6px',
            borderRadius: '4px',
            fontSize: '11px',
            fontFamily: 'monospace',
            fontWeight: 600,
            display: 'inline-block',
            verticalAlign: 'middle',
            margin: '0 2px'
          }}
        >
          {part}
        </span>
      );
    }
    
    return part;
  });
};

export const MarkdownRenderer = ({ content, onLinkClick }) => {
  if (!content) return null;

  // Split by code blocks to separate code from text blocks
  const parts = content.split(/(```[\s\S]*?```)/g);

  return (
    <div className="markdown-body" style={{ color: 'var(--text-main)', fontSize: '14.5px', lineHeight: '1.6', whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
      {parts.map((part, index) => {
        if (part.startsWith('```')) {
          // Parse code block
          const lines = part.split('\n');
          const firstLine = lines[0];
          const lang = firstLine.replace('```', '').trim();
          const code = lines.slice(1, -1).join('\n');
          return (
            <div key={index} style={{ margin: '12px 0', borderRadius: '6px', overflow: 'hidden', border: '1px solid var(--border-color)' }}>
              <div style={{
                backgroundColor: 'rgba(255,255,255,0.03)',
                padding: '6px 12px',
                fontSize: '11px',
                fontFamily: 'monospace',
                color: 'var(--accent-blue)',
                borderBottom: '1px solid var(--border-color)',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                userSelect: 'none'
              }}>
                <span>{(lang || 'CODE').toUpperCase()}</span>
                <span 
                  onClick={() => copyToClipboard(code)}
                  style={{
                    cursor: 'pointer',
                    color: 'var(--text-muted)',
                    fontSize: '10px',
                    fontWeight: 600,
                    transition: 'color 0.2s ease'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.color = 'var(--accent-blue)'}
                  onMouseLeave={(e) => e.currentTarget.style.color = 'var(--text-muted)'}
                >
                  COPY
                </span>
              </div>
              <pre style={{
                margin: 0,
                padding: '12px',
                backgroundColor: 'var(--bg-dark)',
                overflowX: 'auto',
                whiteSpace: 'pre-wrap',
                wordBreak: 'break-all',
                fontSize: '13.5px',
                fontFamily: 'monospace',
                color: '#e2e8f0'
              }}>
                <code>{code}</code>
              </pre>
            </div>
          );
        } else {
          // Process standard text block line by line
          const lines = part.split('\n');
          let inList = false;
          let listType = null; // 'ul' | 'ol'
          let listItems = [];
          let inBlockquote = false;
          let blockquoteLines = [];
          const elements = [];

          const renderList = (items, type, key) => {
            if (type === 'ol') {
              return (
                <ol key={key} style={{ paddingLeft: '20px', margin: '8px 0', listStyleType: 'decimal' }}>
                  {items.map((it, idx) => <li key={idx} style={{ marginBottom: '4px' }}>{parseInline(it, onLinkClick)}</li>)}
                </ol>
              );
            }
            return (
              <ul key={key} style={{ paddingLeft: '20px', margin: '8px 0', listStyleType: 'disc' }}>
                {items.map((it, idx) => <li key={idx} style={{ marginBottom: '4px' }}>{parseInline(it, onLinkClick)}</li>)}
              </ul>
            );
          };

          const renderBlockquote = (lines, key) => {
            const firstLine = lines[0] ? lines[0].trim() : '';
            const alertMatch = firstLine.match(/^\[!(IMPORTANT|NOTE|WARNING|TIP|CAUTION)\]$/i);
            
            let alertType = null;
            let displayLines = lines;
            if (alertMatch) {
              alertType = alertMatch[1].toUpperCase();
              displayLines = lines.slice(1);
            }
            
            let borderColor = 'rgba(255, 255, 255, 0.15)';
            let backgroundColor = 'rgba(255, 255, 255, 0.02)';
            let textColor = 'var(--text-main)';
            let titleColor = 'var(--text-main)';
            let icon = 'ℹ️';
            
            if (alertType === 'IMPORTANT') {
              borderColor = '#a855f7'; // Purple
              backgroundColor = 'rgba(168, 85, 247, 0.07)';
              titleColor = '#c084fc';
              icon = '🚨';
            } else if (alertType === 'NOTE') {
              borderColor = '#3b82f6'; // Blue
              backgroundColor = 'rgba(59, 130, 246, 0.07)';
              titleColor = '#60a5fa';
              icon = 'ℹ️';
            } else if (alertType === 'WARNING') {
              borderColor = '#eab308'; // Yellow
              backgroundColor = 'rgba(234, 179, 8, 0.07)';
              titleColor = '#facc15';
              icon = '⚠️';
            } else if (alertType === 'TIP') {
              borderColor = '#10b981'; // Green
              backgroundColor = 'rgba(16, 185, 129, 0.07)';
              titleColor = '#34d399';
              icon = '💡';
            } else if (alertType === 'CAUTION') {
              borderColor = '#ef4444'; // Red
              backgroundColor = 'rgba(239, 68, 68, 0.07)';
              titleColor = '#f87171';
              icon = '🛑';
            } else {
              // Standard blockquote (blue/cyan scheme default style)
              borderColor = '#00d4ff';
              backgroundColor = 'rgba(0, 212, 255, 0.03)';
              titleColor = '#00d4ff';
              icon = '💬';
            }
            
            return (
              <div 
                key={key} 
                className={`blockquote-callout ${alertType ? alertType.toLowerCase() : 'standard'}`}
                style={{
                  borderLeft: `4px solid ${borderColor}`,
                  backgroundColor: backgroundColor,
                  padding: '12px 16px',
                  margin: '12px 0',
                  borderRadius: '0 8px 8px 0',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '6px',
                  boxShadow: '0 2px 8px rgba(0, 0, 0, 0.15)'
                }}
              >
                {alertType && (
                  <div style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    gap: '6px', 
                    fontSize: '11px', 
                    fontWeight: 700, 
                    color: titleColor,
                    fontFamily: 'monospace',
                    letterSpacing: '1px',
                    textTransform: 'uppercase'
                  }}>
                    <span>{icon}</span>
                    <span>{alertType}</span>
                  </div>
                )}
                <div style={{ color: textColor, fontSize: '13.5px', margin: 0 }}>
                  {displayLines.map((line, idx) => (
                    <p key={idx} style={{ margin: '4px 0', lineBreak: 'anywhere' }}>
                      {parseInline(line, onLinkClick)}
                    </p>
                  ))}
                </div>
              </div>
            );
          };

          for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const trimmed = line.trim();
            const bqMatch = line.match(/^\s*>\s?(.*)$/);

            if (bqMatch) {
              if (inList) {
                elements.push(renderList(listItems, listType, `list-${i}`));
                inList = false;
                listType = null;
                listItems = [];
              }
              if (!inBlockquote) {
                inBlockquote = true;
                blockquoteLines = [];
              }
              blockquoteLines.push(bqMatch[1]);
            } else {
              if (inBlockquote) {
                elements.push(renderBlockquote(blockquoteLines, `bq-${i}`));
                inBlockquote = false;
                blockquoteLines = [];
              }

              // Check list indicators
              const ulMatch = trimmed.match(/^[-*+]\s+(.*)$/);
              const olMatch = trimmed.match(/^(\d+)\.\s+(.*)$/);

              if (ulMatch) {
                if (!inList || listType !== 'ul') {
                  if (inList) elements.push(renderList(listItems, listType, `list-${i}`));
                  inList = true;
                  listType = 'ul';
                  listItems = [];
                }
                listItems.push(ulMatch[1]);
              } else if (olMatch) {
                if (!inList || listType !== 'ol') {
                  if (inList) elements.push(renderList(listItems, listType, `list-${i}`));
                  inList = true;
                  listType = 'ol';
                  listItems = [];
                }
                listItems.push(olMatch[2]);
              } else {
                if (inList) {
                  elements.push(renderList(listItems, listType, `list-${i}`));
                  inList = false;
                  listType = null;
                  listItems = [];
                }

                // Check headers
                const headerMatch = trimmed.match(/^(#{1,6})\s+(.*)$/);
                if (headerMatch) {
                  const level = headerMatch[1].length;
                  const text = headerMatch[2];
                  const fontSize = level === 1 ? '18px' : level === 2 ? '15px' : '13px';
                  const style = { margin: '14px 0 6px 0', fontWeight: 700, color: 'var(--text-main)', display: 'block' };
                  if (level === 1) style.borderBottom = '1px solid var(--border-color)';
                  elements.push(
                    <span key={`h-${i}`} style={{ ...style, fontSize }}>
                      {parseInline(text, onLinkClick)}
                    </span>
                  );
                } else if (trimmed === '---') {
                  elements.push(<hr key={`hr-${i}`} style={{ border: 'none', borderTop: '1px solid var(--border-color)', margin: '14px 0' }} />);
                } else if (trimmed) {
                  elements.push(<p key={`p-${i}`} style={{ margin: '6px 0' }}>{parseInline(line, onLinkClick)}</p>);
                }
              }
            }
          }

          if (inList) {
            elements.push(renderList(listItems, listType, `list-end`));
          }
          if (inBlockquote) {
            elements.push(renderBlockquote(blockquoteLines, `bq-end`));
          }

          return <React.Fragment key={index}>{elements}</React.Fragment>;
        }
      })}
    </div>
  );
};
