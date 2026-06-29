import React, { useState, useEffect } from 'react';
import { Expand, Download, FileText, Copy, ChevronRight, Folder, Pin, Trash2, Volume2, Square } from 'lucide-react';
import { MarkdownRenderer } from './MarkdownRenderer';

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

const ArchivePanel = ({ width, onClose, activeModule, activeChatId, selectedFilePath, onSelectFile, voiceState = 'idle' }) => {
  const [files, setFiles] = useState([]);
  const [selectedFileContent, setSelectedFileContent] = useState('');
  const [selectedFileName, setSelectedFileName] = useState('');
  const [selectedFiles, setSelectedFiles] = useState([]);

  const toggleSelectFile = (path) => {
    setSelectedFiles(prev => 
      prev.includes(path) ? prev.filter(p => p !== path) : [...prev, path]
    );
  };

  const handleDeleteSelected = async () => {
    if (selectedFiles.length === 0) return;
    if (!window.confirm(`Are you sure you want to delete the ${selectedFiles.length} selected files?`)) {
      return;
    }
    
    let successCount = 0;
    for (const path of selectedFiles) {
      try {
        const cleanPath = path.replace(/^file:\/\/\/?/, '');
        const res = await fetch(`/api/archive/file?path=${encodeURIComponent(cleanPath)}`, {
          method: 'DELETE'
        });
        if (res.ok) {
          successCount++;
          // Remove from local states
          setFiles(prev => prev.filter(f => f.path !== path));
          setPinnedFiles(prev => prev.filter(f => f.path !== path));
          if (selectedFilePath === path) {
            onSelectFile(null);
          }
        }
      } catch (err) {
        console.error('Error deleting file:', path, err);
      }
    }
    
    setSelectedFiles([]);
  };

  const handleDeleteFile = async (file) => {
    if (!window.confirm(`Are you sure you want to delete ${file.name}?`)) {
      return;
    }
    
    try {
      const cleanPath = file.path.replace(/^file:\/\/\/?/, '');
      const res = await fetch(`/api/archive/file?path=${encodeURIComponent(cleanPath)}`, {
        method: 'DELETE'
      });
      if (res.ok) {
        setFiles(prev => prev.filter(f => f.path !== file.path));
        setPinnedFiles(prev => prev.filter(f => f.path !== file.path));
        setSelectedFiles(prev => prev.filter(p => p !== file.path));
        if (selectedFilePath === file.path) {
          onSelectFile(null);
        }
      } else {
        alert('Failed to delete file');
      }
    } catch (err) {
      console.error('Error deleting file:', err);
      alert('Error deleting file: ' + err.message);
    }
  };

  // Local storage state for pinned archives
  const [pinnedFiles, setPinnedFiles] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('aida_pinned_archives') || '[]');
    } catch (e) {
      return [];
    }
  });

  useEffect(() => {
    localStorage.setItem('aida_pinned_archives', JSON.stringify(pinnedFiles));
  }, [pinnedFiles]);

  const togglePin = (file) => {
    const isPinned = pinnedFiles.some(f => f.path === file.path);
    if (isPinned) {
      setPinnedFiles(pinnedFiles.filter(f => f.path !== file.path));
    } else {
      setPinnedFiles([...pinnedFiles, file]);
    }
  };

  const isCodeFile = (filename) => {
    return /\.(jsx|py|json|js|css|md|txt)$/i.test(filename);
  };

  const handleSpeakFile = async () => {
    if (!selectedFilePath) return;
    try {
      const res = await fetch('/api/voice/speak-file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: selectedFilePath })
      });
      if (!res.ok) {
        console.error('Failed to trigger readout');
      }
    } catch (err) {
      console.error('Error triggering speak-file:', err);
    }
  };

  const handleAbortVoice = async () => {
    try {
      const res = await fetch('/api/voice/abort', {
        method: 'POST'
      });
      if (!res.ok) {
        console.error('Failed to abort voice readout');
      }
    } catch (err) {
      console.error('Error aborting voice readout:', err);
    }
  };

  // Fetch archives list on activeModule/activeChatId changes
  useEffect(() => {
    if (!activeModule) {
      setFiles([]);
      return;
    }
    const fetchFiles = async () => {
      try {
        const url = activeChatId 
          ? `/api/archive/files?module_id=${activeModule}&chat_id=${activeChatId}`
          : `/api/archive/files?module_id=${activeModule}`;
        const res = await fetch(url);
        if (res.ok) {
          const data = await res.json();
          setFiles(data);
        }
      } catch (err) {
        console.error('Error fetching archive files:', err);
      }
    };
    fetchFiles();
  }, [activeModule, activeChatId]);

  // Fetch content on selectedFilePath changes
  useEffect(() => {
    if (!selectedFilePath) {
      setSelectedFileContent('');
      setSelectedFileName('');
      return;
    }

    const fetchContent = async () => {
      try {
        const name = selectedFilePath.split(/[/\\]/).pop();
        setSelectedFileName(name);

        const cleanPath = selectedFilePath.replace(/^file:\/\/\/?/, '');
        const res = await fetch(`/api/archive/file?path=${encodeURIComponent(cleanPath)}`);
        if (res.ok) {
          const data = await res.json();
          setSelectedFileContent(data.content);
        } else {
          setSelectedFileContent(`Error loading file: ${res.statusText}`);
        }
      } catch (err) {
        setSelectedFileContent(`Error fetching file: ${err.message}`);
      }
    };

    fetchContent();
  }, [selectedFilePath]);

  return (
    <div className="panel" style={{ 
      width: `${width}px`, 
      flexShrink: 0,
      height: '100%', 
      borderLeft: '1px solid var(--border-color)', 
      position: 'relative',
      overflow: 'hidden'
    }}>
      <div style={{ position: 'absolute', top: '8px', left: '8px', cursor: 'pointer', zIndex: 10 }} onClick={onClose}>
        <ChevronRight size={16} color="var(--text-muted)" />
      </div>

      {/* Header static title */}
      <div style={{
        borderBottom: '1px solid var(--border-color)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '48px',
        flexShrink: 0,
        backgroundColor: 'rgba(0,0,0,0.1)',
        fontSize: '11px',
        fontWeight: 600,
        color: 'var(--text-main)',
        letterSpacing: '1.2px',
        fontFamily: 'monospace'
      }}>
        ARCHIVES
      </div>

      {/* Sliding Wrapper */}
      <div style={{
        display: 'flex',
        width: '200%',
        height: 'calc(100% - 48px)',
        transform: selectedFilePath ? 'translateX(-50%)' : 'translateX(0%)',
        transition: 'transform 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
      }}>
        {/* Slide 1: Module Grid (List) */}
        <div style={{ width: '50%', height: '100%', padding: '16px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          
          {selectedFiles.length > 0 && (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              padding: '8px 12px',
              backgroundColor: 'rgba(239, 68, 68, 0.08)',
              border: '1px solid rgba(239, 68, 68, 0.25)',
              borderRadius: '6px',
              flexShrink: 0
            }}>
              <span style={{ fontSize: '11px', fontFamily: 'monospace', color: '#f87171', fontWeight: 600 }}>
                {selectedFiles.length} SELECTED
              </span>
              <div style={{ display: 'flex', gap: '6px' }}>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    const allPaths = [...pinnedFiles.map(f => f.path), ...files.map(f => f.path)];
                    setSelectedFiles(allPaths);
                  }}
                  style={{
                    backgroundColor: 'transparent',
                    border: '1px solid var(--border-color)',
                    color: 'var(--text-main)',
                    padding: '2px 8px',
                    borderRadius: '4px',
                    fontSize: '10px',
                    fontFamily: 'monospace',
                    cursor: 'pointer',
                    transition: 'all 0.2s'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.borderColor = 'var(--text-main)'}
                  onMouseLeave={(e) => e.currentTarget.style.borderColor = 'var(--border-color)'}
                >
                  ALL
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedFiles([]);
                  }}
                  style={{
                    backgroundColor: 'transparent',
                    border: '1px solid var(--border-color)',
                    color: 'var(--text-muted)',
                    padding: '2px 8px',
                    borderRadius: '4px',
                    fontSize: '10px',
                    fontFamily: 'monospace',
                    cursor: 'pointer',
                    transition: 'all 0.2s'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.borderColor = 'var(--text-muted)'}
                  onMouseLeave={(e) => e.currentTarget.style.borderColor = 'var(--border-color)'}
                >
                  CLEAR
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDeleteSelected();
                  }}
                  style={{
                    backgroundColor: '#ef4444',
                    border: 'none',
                    color: '#fff',
                    padding: '2px 8px',
                    borderRadius: '4px',
                    fontSize: '10px',
                    fontFamily: 'monospace',
                    fontWeight: 'bold',
                    cursor: 'pointer',
                    transition: 'all 0.2s'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#dc2626'}
                  onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#ef4444'}
                >
                  DELETE
                </button>
              </div>
            </div>
          )}
          
          {/* Pinned Archives Section */}
          {pinnedFiles.length > 0 && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <div style={{ fontSize: '10px', color: 'var(--accent-blue)', fontWeight: 600, letterSpacing: '1.2px', fontFamily: 'monospace', paddingLeft: '4px' }}>
                PINNED ARCHIVES
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {pinnedFiles.map(file => (
                  <div 
                    key={`pinned-${file.path}`} 
                    className="archive-folder-box"
                    onClick={() => onSelectFile(file.path)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      padding: '8px 12px',
                      borderRadius: '6px',
                      backgroundColor: 'rgba(0, 212, 255, 0.03)',
                      border: '1px solid rgba(0, 212, 255, 0.15)',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.borderColor = 'var(--accent-blue)';
                      e.currentTarget.style.backgroundColor = 'rgba(0, 212, 255, 0.06)';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.borderColor = 'rgba(0, 212, 255, 0.15)';
                      e.currentTarget.style.backgroundColor = 'rgba(0, 212, 255, 0.03)';
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', minWidth: 0, flex: 1 }}>
                      <input 
                        type="checkbox"
                        checked={selectedFiles.includes(file.path)}
                        onClick={(e) => e.stopPropagation()}
                        onChange={() => toggleSelectFile(file.path)}
                        style={{
                          marginRight: '2px',
                          cursor: 'pointer',
                          accentColor: 'var(--accent-blue)'
                        }}
                      />
                      {isCodeFile(file.name) ? (
                        <FileText size={16} color="var(--accent-blue)" style={{ flexShrink: 0 }} />
                      ) : (
                        <Folder size={16} color="var(--accent-gold)" style={{ flexShrink: 0 }} />
                      )}
                      <span style={{ fontSize: '11px', fontFamily: 'monospace', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', color: 'var(--text-main)' }}>
                        {file.name}
                      </span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', flexShrink: 0 }}>
                      <Pin 
                        size={13} 
                        color="var(--accent-blue)" 
                        fill="var(--accent-blue)"
                        style={{ cursor: 'pointer' }} 
                        onClick={(e) => {
                          e.stopPropagation();
                          togglePin(file);
                        }}
                      />
                      <Trash2 
                        size={13} 
                        color="#ef4444" 
                        style={{ cursor: 'pointer', transition: 'color 0.2s' }} 
                        onMouseEnter={(e) => e.currentTarget.style.color = '#f87171'}
                        onMouseLeave={(e) => e.currentTarget.style.color = '#ef4444'}
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDeleteFile(file);
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Module Archives Section */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <div style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: 600, letterSpacing: '1.2px', fontFamily: 'monospace', paddingLeft: '4px' }}>
              {activeModule ? `${activeModule.toUpperCase()} ARCHIVES` : 'ARCHIVES'}
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {files.length === 0 ? (
                <div style={{ fontSize: '11px', color: 'var(--text-muted)', textAlign: 'center', marginTop: '10px', fontFamily: 'monospace' }}>
                  NO ARCHIVES AVAILABLE
                </div>
              ) : (
                files.map(file => {
                  const isPinned = pinnedFiles.some(f => f.path === file.path);
                  return (
                    <div 
                      key={file.path} 
                      className="archive-folder-box"
                      onClick={() => onSelectFile(file.path)}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        padding: '8px 12px',
                        borderRadius: '6px',
                        backgroundColor: 'rgba(255,255,255,0.02)',
                        border: '1px solid rgba(255,255,255,0.05)',
                        cursor: 'pointer',
                        transition: 'all 0.2s ease'
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.borderColor = 'var(--accent-blue)';
                        e.currentTarget.style.backgroundColor = 'rgba(0, 212, 255, 0.04)';
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.borderColor = 'rgba(255,255,255,0.05)';
                        e.currentTarget.style.backgroundColor = 'rgba(255,255,255,0.02)';
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', minWidth: 0, flex: 1 }}>
                        <input 
                          type="checkbox"
                          checked={selectedFiles.includes(file.path)}
                          onClick={(e) => e.stopPropagation()}
                          onChange={() => toggleSelectFile(file.path)}
                          style={{
                            marginRight: '2px',
                            cursor: 'pointer',
                            accentColor: 'var(--accent-blue)'
                          }}
                        />
                        {isCodeFile(file.name) ? (
                          <FileText size={16} color="var(--accent-blue)" style={{ flexShrink: 0 }} />
                        ) : (
                          <Folder size={16} color="var(--accent-gold)" style={{ flexShrink: 0 }} />
                        )}
                        <span style={{ fontSize: '11px', fontFamily: 'monospace', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', color: 'var(--text-main)' }}>
                          {file.name}
                        </span>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '6px', flexShrink: 0 }}>
                        <Pin 
                          size={13} 
                          color={isPinned ? 'var(--accent-blue)' : 'var(--text-muted)'} 
                          fill={isPinned ? 'var(--accent-blue)' : 'none'}
                          style={{ cursor: 'pointer', transition: 'all 0.2s' }} 
                          onClick={(e) => {
                            e.stopPropagation();
                            togglePin(file);
                          }}
                        />
                        <Trash2 
                          size={13} 
                          color="#ef4444" 
                          style={{ cursor: 'pointer', transition: 'color 0.2s' }} 
                          onMouseEnter={(e) => e.currentTarget.style.color = '#f87171'}
                          onMouseLeave={(e) => e.currentTarget.style.color = '#ef4444'}
                          onClick={(e) => {
                            e.stopPropagation();
                            handleDeleteFile(file);
                          }}
                        />
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>
        </div>

        {/* Slide 2: Details Writing */}
        <div style={{ width: '50%', height: '100%', padding: '16px', overflowY: 'auto', display: 'flex', flexDirection: 'column' }}>
          <div style={{
            backgroundColor: '#0d0d10',
            border: '1px solid rgba(0, 212, 255, 0.15)',
            borderLeft: '4px solid var(--accent-blue)',
            borderRadius: '6px',
            padding: '16px',
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            boxShadow: '0 12px 36px rgba(0, 0, 0, 0.65), inset 0 1px 0 rgba(255,255,255,0.03)',
            position: 'relative'
          }}>
            {/* Header / Tab Row */}
            <div style={{
              display: 'flex', 
              justifyContent: 'space-between', 
              alignItems: 'center',
              borderBottom: '1px solid rgba(255,255,255,0.06)',
              paddingBottom: '12px',
              marginBottom: '12px',
              flexShrink: 0
            }}>
              <button 
                onClick={() => onSelectFile(null)}
                style={{
                  backgroundColor: 'rgba(239, 68, 68, 0.06)',
                  border: '1px solid rgba(239, 68, 68, 0.25)',
                  color: '#f87171',
                  padding: '4px 10px',
                  borderRadius: '4px',
                  fontSize: '10.5px',
                  fontWeight: 'bold',
                  fontFamily: 'monospace',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px',
                  transition: 'all 0.2s ease'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.backgroundColor = 'rgba(239, 68, 68, 0.15)';
                  e.currentTarget.style.borderColor = '#ef4444';
                  e.currentTarget.style.boxShadow = '0 0 8px rgba(239, 68, 68, 0.3)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.backgroundColor = 'rgba(239, 68, 68, 0.06)';
                  e.currentTarget.style.borderColor = 'rgba(239, 68, 68, 0.25)';
                  e.currentTarget.style.boxShadow = 'none';
                }}
              >
                ✕ CLOSE
              </button>

              <span style={{
                fontSize: '11px',
                color: '#00d4ff',
                fontFamily: 'monospace',
                backgroundColor: 'rgba(0, 212, 255, 0.06)',
                border: '1px solid rgba(0, 212, 255, 0.2)',
                padding: '4px 10px',
                borderRadius: '4px',
                fontWeight: 600,
                letterSpacing: '0.5px',
                maxWidth: '130px',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap'
              }} title={selectedFileName}>
                {selectedFileName}
              </span>

              <div style={{display: 'flex', gap: '10px', alignItems: 'center'}}>
                {(() => {
                  const isCurrentPinned = pinnedFiles.some(f => f.path === selectedFilePath);
                  const currentFileObj = { name: selectedFileName, path: selectedFilePath, type: 'code' };
                  return (
                    <Pin 
                      size={14} 
                      color={isCurrentPinned ? 'var(--accent-blue)' : 'var(--text-muted)'} 
                      fill={isCurrentPinned ? 'var(--accent-blue)' : 'none'}
                      style={{cursor: 'pointer', transition: 'all 0.2s'}} 
                      title={isCurrentPinned ? 'Unpin' : 'Pin'}
                      onClick={() => togglePin(currentFileObj)} 
                    />
                  );
                })()}

                {voiceState === 'speaking' ? (
                  <>
                    <style dangerouslySetInnerHTML={{__html: `
                      @keyframes pulse-red {
                        0% { opacity: 0.5; filter: drop-shadow(0 0 1px #ef4444); }
                        50% { opacity: 1; filter: drop-shadow(0 0 6px #ef4444); }
                        100% { opacity: 0.5; filter: drop-shadow(0 0 1px #ef4444); }
                      }
                    `}} />
                    <Square 
                      size={14} 
                      color="#ef4444" 
                      style={{cursor: 'pointer', animation: 'pulse-red 1.5s infinite'}} 
                      title="Stop Read Out Loud" 
                      onClick={handleAbortVoice}
                    />
                  </>
                ) : (
                  <Volume2 
                    size={14} 
                    color="var(--text-muted)" 
                    style={{cursor: 'pointer', transition: 'color 0.2s'}} 
                    onMouseEnter={(e) => e.currentTarget.style.color = '#00d4ff'}
                    onMouseLeave={(e) => e.currentTarget.style.color = 'var(--text-muted)'}
                    title="Read Out Loud (Voice Chat)" 
                    onClick={handleSpeakFile}
                  />
                )}

                <Copy 
                  size={14} 
                  color="var(--text-muted)" 
                  style={{cursor: 'pointer', transition: 'color 0.2s'}} 
                  onMouseEnter={(e) => e.currentTarget.style.color = '#00d4ff'}
                  onMouseLeave={(e) => e.currentTarget.style.color = 'var(--text-muted)'}
                  title="Copy Content" 
                  onClick={() => copyToClipboard(selectedFileContent)} 
                />
              </div>
            </div>

            {/* Sub-header details */}
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              fontSize: '9.5px',
              fontFamily: 'monospace',
              color: 'var(--text-muted)',
              marginBottom: '10px',
              padding: '0 2px'
            }}>
              <span>FORMAT: MARKDOWN</span>
              <span>READ-ONLY STREAM</span>
            </div>
            
            {/* Rendered Text Area */}
            <div style={{
              flex: 1,
              overflowY: 'auto',
              scrollbarWidth: 'thin',
              paddingRight: '6px'
            }}>
              <MarkdownRenderer content={selectedFileContent} onLinkClick={onSelectFile} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ArchivePanel;
