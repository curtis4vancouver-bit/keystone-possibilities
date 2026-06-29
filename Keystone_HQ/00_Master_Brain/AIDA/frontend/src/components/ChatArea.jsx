import React from 'react';
import { Send, Mic, Paperclip, ChevronDown, Menu, PanelRightOpen, Sparkles, FileText, Folder, RefreshCw } from 'lucide-react';
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

// Zero-dependency Markdown rendering component for AIDA chat
// Reusable MarkdownRenderer is imported from './MarkdownRenderer'

const ChatArea = ({ onOpenSidebar, onOpenArchive, isSidebarOpen, isArchiveOpen, messages, archivedMessages = [], onSendMessage, activeModule, onOpenFile, activeChatId, voiceBridgeStatus = 'disconnected', voiceState = 'idle', onToggleVoice, isLocalListening = false, onLocalListeningChange, isAgentWorking = false, activeAgentsCount = 0, isPythonWorking = false, activePythonTasksCount = 0 }) => {
  const [isDragging, setIsDragging] = React.useState(false);
  const [inputText, setInputText] = React.useState('');
  const [activeTab, setActiveTab] = React.useState('chat');
  const [bootstrapText, setBootstrapText] = React.useState('');
  const [uploadedFiles, setUploadedFiles] = React.useState([]);

  const [activeJobSite, setActiveJobSite] = React.useState('Select Job Site');
  const jobSites = [
    'Select Job Site',
    'Site 1: 101 Main St (Whistler)',
    'Site 2: BC Hydro Substation Alpha',
    'Site 3: Pemberton New Build'
  ];

  const handleJobSiteChange = (e) => {
    const site = e.target.value;
    setActiveJobSite(site);
    if (site !== 'Select Job Site') {
      onSendMessage(`[SYSTEM CONTEXT OVERRIDE]: Wayne has actively selected the following job site in the UI: **${site}**. From now on, all questions, code checks, and documentation must be implicitly focused on this job site until he changes it.`);
    }
  };

  const [activeTaxLedger, setActiveTaxLedger] = React.useState('Select Brand Ledger');
  const taxLedgers = [
    'Select Brand Ledger',
    'Keystone Possibilities (Construction)',
    'Keystone Recomposition (Health/Media)',
    'Shared / Cross-Brand Allocation'
  ];

  const handleTaxLedgerChange = (e) => {
    const ledger = e.target.value;
    setActiveTaxLedger(ledger);
    if (ledger !== 'Select Brand Ledger') {
      onSendMessage(`[SYSTEM CONTEXT OVERRIDE]: Wayne has actively selected the following Brand Ledger in the UI: **${ledger}**. From now on, all tax categorization, write-offs, and financial questions must be implicitly focused on this entity until he changes it.`);
    }
  };

  const [activeWealthVector, setActiveWealthVector] = React.useState('Select Wealth Vector');
  const wealthVectors = [
    'Select Wealth Vector',
    'Polymarket & Digital Assets',
    'Brand Monetization & Retreats',
    'Career Strategy & Capital Savings'
  ];

  const handleWealthVectorChange = (e) => {
    const vector = e.target.value;
    setActiveWealthVector(vector);
    if (vector !== 'Select Wealth Vector') {
      onSendMessage(`[SYSTEM CONTEXT OVERRIDE]: Wayne has actively selected the following Wealth Vector in the UI: **${vector}**. From now on, all market analysis, predictions, and financial advice must be implicitly focused on this strategy until he changes it.`);
    }
  };

  const [activeResearchVector, setActiveResearchVector] = React.useState('Select Research Vector');
  const researchVectors = [
    'Select Research Vector',
    'Cutting-Edge AI & New MCPs',
    'Code, SEO & Website Infrastructure',
    'YouTube Production & Media Automations',
    'Wealth, Financials & Operations'
  ];

  const handleResearchVectorChange = (e) => {
    const vector = e.target.value;
    setActiveResearchVector(vector);
    if (vector !== 'Select Research Vector') {
      onSendMessage(`[SYSTEM CONTEXT OVERRIDE]: Wayne has actively selected the following Research Vector in the UI: **${vector}**. From now on, all autonomous rabbit holes, tech scouting, and code verification must be focused exclusively on this domain until he changes it.`);
    }
  };

  const [isCommittingLearning, setIsCommittingLearning] = React.useState(false);
  const [committedRuleId, setCommittedRuleId] = React.useState(null);
  const [commitError, setCommitError] = React.useState(null);

  const openFolder = async (folderPath) => {
    try {
      const res = await fetch('/api/open-folder', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: folderPath })
      });
      if (!res.ok) {
        const text = await res.text();
        console.error(`Failed to open folder: ${res.status} - ${text}`);
      }
    } catch (err) {
      console.error("Failed to open folder", err);
    }
  };

  const [isSyncingDrive, setIsSyncingDrive] = React.useState(false);
  const [syncStatus, setSyncStatus] = React.useState(null);

  const handleSyncDrive = async () => {
    setIsSyncingDrive(true);
    setSyncStatus('syncing');
    try {
      const res = await fetch('/api/sync/drive', {
        method: 'POST'
      });
      if (res.ok) {
        setSyncStatus('synced');
        setTimeout(() => setSyncStatus(null), 4000);
      } else {
        setSyncStatus('failed');
        setTimeout(() => setSyncStatus(null), 4000);
      }
    } catch (err) {
      console.error(err);
      setSyncStatus('failed');
      setTimeout(() => setSyncStatus(null), 4000);
    } finally {
      setIsSyncingDrive(false);
    }
  };

  const handleCommitLearningAuto = async () => {
    if (!activeChatId) {
      alert("No active chat conversation detected.");
      return;
    }
    setIsCommittingLearning(true);
    setCommitError(null);
    setCommittedRuleId(null);
    try {
      const res = await fetch(`/api/learn/commit-auto?chat_id=${activeChatId}`, {
        method: 'POST'
      });
      if (res.ok) {
        const data = await res.json();
        if (data.success && data.rule_id) {
          setCommittedRuleId(data.rule_id);
          // Revert visual state after 4 seconds
          setTimeout(() => {
            setCommittedRuleId(null);
          }, 4000);
        } else {
          setCommitError("Commit failed");
          setTimeout(() => setCommitError(null), 4000);
        }
      } else {
        const errText = await res.text();
        setCommitError("Failed: " + errText);
        setTimeout(() => setCommitError(null), 4000);
      }
    } catch (err) {
      console.error(err);
      setCommitError("Error: " + err.message);
      setTimeout(() => setCommitError(null), 4000);
    } finally {
      setIsCommittingLearning(false);
    }
  };

  const messagesEndRef = React.useRef(null);
  const scrollContainerRef = React.useRef(null);
  const fileInputRef = React.useRef(null);

  // Keep latest states in refs to avoid closure issues in SpeechRecognition handlers
  const inputTextRef = React.useRef(inputText);
  React.useEffect(() => {
    inputTextRef.current = inputText;
  }, [inputText]);

  const uploadedFilesRef = React.useRef(uploadedFiles);
  React.useEffect(() => {
    uploadedFilesRef.current = uploadedFiles;
  }, [uploadedFiles]);

  const onSendMessageRef = React.useRef(onSendMessage);
  React.useEffect(() => {
    onSendMessageRef.current = onSendMessage;
  }, [onSendMessage]);

  const recognitionRef = React.useRef(null);
  const isListeningRef = React.useRef(false);
  const shouldSubmitRef = React.useRef(false);

  const isF9PressedRef = React.useRef(false);

  const startLocalListening = () => {
    if (recognitionRef.current && !isListeningRef.current) {
      shouldSubmitRef.current = false;
      isListeningRef.current = true;
      if (onLocalListeningChange) {
        onLocalListeningChange(true);
      }
      try {
        recognitionRef.current.start();
      } catch (err) {
        console.error('Failed to start speech recognition:', err);
      }
    }
  };

  const stopLocalListening = (submit = true) => {
    if (recognitionRef.current && isListeningRef.current) {
      shouldSubmitRef.current = submit;
      try {
        recognitionRef.current.stop();
      } catch (err) {
        console.error('Failed to stop speech recognition:', err);
      }
      isListeningRef.current = false;
      if (onLocalListeningChange) {
        onLocalListeningChange(false);
      }
    }
  };

  React.useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const rec = new SpeechRecognition();
      rec.continuous = true;
      rec.interimResults = true;
      rec.lang = 'en-US';
      
      let finalTranscript = '';

      rec.onstart = () => {
        finalTranscript = '';
      };

      rec.onresult = (event) => {
        let interimTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript;
          } else {
            interimTranscript += event.results[i][0].transcript;
          }
        }
        setInputText(finalTranscript + interimTranscript);
      };

      rec.onerror = (e) => {
        console.error('Speech recognition error:', e);
      };

      rec.onend = () => {
        if (onLocalListeningChange) {
          onLocalListeningChange(false);
        }
        isListeningRef.current = false;
        
        const text = inputTextRef.current;
        const files = uploadedFilesRef.current;
        if (text.trim() || files.length > 0) {
          let messageText = text;
          if (files.length > 0) {
            const fileListStr = files.map(f => `[Uploaded File]: ${f.name}\nSaved to: ${f.path}`).join('\n\n');
            if (messageText.trim()) {
              messageText = `${messageText}\n\n${fileListStr}`;
            } else {
              messageText = fileListStr;
            }
          }
          if (onSendMessageRef.current) {
            onSendMessageRef.current(messageText);
          }
          setInputText('');
          setUploadedFiles([]);
        }
      };

      recognitionRef.current = rec;
    }
  }, []);

  React.useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'F8') {
        e.preventDefault();
        startLocalListening();
      } else if (e.key === 'F9') {
        e.preventDefault();
        if (!isF9PressedRef.current) {
          isF9PressedRef.current = true;
          fetch('/api/voice/press', { method: 'POST' }).catch(err => console.error(err));
        }
      }
    };

    const handleKeyUp = (e) => {
      if (e.key === 'F8') {
        e.preventDefault();
        stopLocalListening(true);
      } else if (e.key === 'F9') {
        e.preventDefault();
        if (isF9PressedRef.current) {
          isF9PressedRef.current = false;
          fetch('/api/voice/release', { method: 'POST' }).catch(err => console.error(err));
        }
      }
    };

    const handleBlur = () => {
      if (isListeningRef.current) {
        stopLocalListening(true);
      }
      if (isF9PressedRef.current) {
        isF9PressedRef.current = false;
        fetch('/api/voice/release', { method: 'POST' }).catch(err => console.error(err));
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);
    window.addEventListener('blur', handleBlur);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
      window.removeEventListener('blur', handleBlur);
    };
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const prevMessagesLengthRef = React.useRef(messages.length);

  React.useEffect(() => {
    const prevLength = prevMessagesLengthRef.current;
    prevMessagesLengthRef.current = messages.length;

    const el = scrollContainerRef.current;
    if (!el) return;

    const threshold = 100;
    const isAtBottom = el.scrollHeight - el.scrollTop - el.clientHeight <= threshold;

    const hasNewMessage = messages.length > prevLength;
    const lastMessage = messages[messages.length - 1];
    const userJustSent = lastMessage && lastMessage.sender === 'user';

    if (hasNewMessage || userJustSent || isAtBottom) {
      scrollToBottom();
    }
  }, [messages]);

  React.useEffect(() => {
    if (activeModule) {
      setBootstrapText('Loading bootstrap script...');
      fetch(`/api/bootstrap/${activeModule}`)
        .then(res => res.ok ? res.json() : null)
        .then(data => {
          if (data && data.prompt) {
            setBootstrapText(data.prompt);
          }
        })
        .catch(err => {
          console.error(err);
          setBootstrapText(`Error loading bootstrap for ${activeModule}`);
        });
    } else {
      setBootstrapText('');
    }
  }, [activeModule]);

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDragEnter = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    if (e.currentTarget.contains(e.relatedTarget)) return;
    setIsDragging(false);
  };

  const uploadFile = async (file) => {
    if (!file) return;
    try {
      const formData = new FormData();
      formData.append('file', file);
      if (activeChatId) {
        formData.append('chat_id', activeChatId);
      }
      
      const res = await fetch('/api/upload', {
        method: 'POST',
        body: formData
      });
      
      if (res.ok) {
        const data = await res.json();
        // Add to staged files instead of immediately sending
        setUploadedFiles(prev => [...prev, { name: data.filename, path: data.path }]);
      } else {
        const errData = await res.json();
        console.error('File upload failed:', errData);
        alert(`Upload failed: ${errData.detail || 'Unknown error'}`);
      }
    } catch (err) {
      console.error('Error uploading file:', err);
      alert(`Error uploading file: ${err.message}`);
    }
  };

  const handlePaste = (e) => {
    const items = e.clipboardData?.items;
    if (items) {
      for (let i = 0; i < items.length; i++) {
        if (items[i].type.indexOf('image') !== -1) {
          const file = items[i].getAsFile();
          if (file) {
            const timestamp = new Date().getTime();
            const renamedFile = new File([file], `screenshot_${timestamp}.png`, { type: file.type });
            uploadFile(renamedFile);
          }
        }
      }
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      for (let i = 0; i < files.length; i++) {
        uploadFile(files[i]);
      }
    }
  };

  const handleFileChange = (e) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      for (let i = 0; i < files.length; i++) {
        uploadFile(files[i]);
      }
    }
  };


  const handleSubmit = () => {
    if (!inputText.trim() && uploadedFiles.length === 0) return;
    
    let messageText = inputText;
    if (uploadedFiles.length > 0) {
      const fileListStr = uploadedFiles.map(f => `[Uploaded File]: ${f.name}\nSaved to: ${f.path}`).join('\n\n');
      if (messageText.trim()) {
        messageText = `${messageText}\n\n${fileListStr}`;
      } else {
        messageText = fileListStr;
      }
    }
    
    onSendMessage(messageText);
    setInputText('');
    setUploadedFiles([]);
  };

  const handleInputKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div 
      onDragOver={handleDragOver}
      onDragEnter={handleDragEnter}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onPaste={handlePaste}
      style={{ flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column', backgroundColor: 'var(--bg-dark)', position: 'relative' }}
    >
      
      {/* Global Drag & Drop Glass Overlay */}
      {isDragging && (
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(10, 20, 35, 0.9)',
          border: '2px dashed var(--accent-blue)',
          borderRadius: '8px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
          backdropFilter: 'blur(8px)',
          pointerEvents: 'none'
        }}>
          <h2 style={{ color: 'var(--accent-blue)', fontFamily: 'monospace', letterSpacing: '2px', marginBottom: '8px' }}>
            DROP FILE TO INGEST
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '13px' }}>
            Document will be processed and stored in Vector Brain namespace
          </p>
        </div>
      )}

      {/* Top Header Bar */}
      <div style={{
        height: '48px',
        borderBottom: '1px solid var(--border-color)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 16px',
        backgroundColor: 'var(--bg-panel)',
        zIndex: 90,
        flexShrink: 0
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          {/* Menu button if sidebar is closed */}
          {!isSidebarOpen && (
            <Menu 
              size={18} 
              color="var(--text-muted)" 
              style={{ cursor: 'pointer', marginRight: '8px' }} 
              onClick={onOpenSidebar} 
            />
          )}
          <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-main)', letterSpacing: '0.5px', fontFamily: 'monospace' }}>
            {activeModule ? (
              {
                chronos: 'Chronos (Master Brain)',
                recomposition: 'Keystone Recomposition (Music)',
                protocols: 'Keystone Protocols (Wellness)',
                possibilities: 'Keystone Possibilities (PM)',
                webmaster: 'Websites, SEO & GEO',
                wayne_health: 'Wayne Stevenson (Health)',
                site_super: 'Site Superintendent (Work)',
                tax_finance: 'Tax Strategist & Finance',
                market_analyst: 'Market Analyst (Wealth)',
                self_evolution: 'Self-Evolution & Learning',
                legacy_archive: 'Legacy Chat Archive'
              }[activeModule] || activeModule
            ).toUpperCase() : 'NO ACTIVE MODULE'}
          </span>
          <span style={{ 
            fontSize: '9px', 
            padding: '2px 6px', 
            borderRadius: '4px', 
            backgroundColor: 'rgba(16, 185, 129, 0.1)', 
            color: 'var(--accent-green)',
            border: '1px solid rgba(16, 185, 129, 0.2)',
            fontFamily: 'monospace',
            marginLeft: '4px'
          }}>
            ACTIVE
          </span>
          {activeModule === 'site_super' && (
            <select
              value={activeJobSite}
              onChange={handleJobSiteChange}
              style={{
                marginLeft: '12px',
                backgroundColor: 'rgba(0, 212, 255, 0.08)',
                border: '1px solid rgba(0, 212, 255, 0.25)',
                color: 'var(--accent-blue)',
                padding: '4px 8px',
                borderRadius: '4px',
                fontSize: '11px',
                fontFamily: 'monospace',
                fontWeight: 600,
                outline: 'none',
                cursor: 'pointer'
              }}
            >
              {jobSites.map((site, idx) => (
                <option key={idx} value={site} style={{ backgroundColor: 'var(--bg-panel)', color: 'var(--text-main)' }}>
                  {site}
                </option>
              ))}
            </select>
          )}
          {activeModule === 'tax_finance' && (
            <select
              value={activeTaxLedger}
              onChange={handleTaxLedgerChange}
              style={{
                marginLeft: '12px',
                backgroundColor: 'rgba(234, 179, 8, 0.08)',
                border: '1px solid rgba(234, 179, 8, 0.25)',
                color: 'var(--accent-yellow)',
                padding: '4px 8px',
                borderRadius: '4px',
                fontSize: '11px',
                fontFamily: 'monospace',
                fontWeight: 600,
                outline: 'none',
                cursor: 'pointer'
              }}
            >
              {taxLedgers.map((ledger, idx) => (
                <option key={idx} value={ledger} style={{ backgroundColor: 'var(--bg-panel)', color: 'var(--text-main)' }}>
                  {ledger}
                </option>
              ))}
            </select>
          )}
          {activeModule === 'market_analyst' && (
            <select
              value={activeWealthVector}
              onChange={handleWealthVectorChange}
              style={{
                marginLeft: '12px',
                backgroundColor: 'rgba(168, 85, 247, 0.08)',
                border: '1px solid rgba(168, 85, 247, 0.25)',
                color: 'var(--accent-purple)',
                padding: '4px 8px',
                borderRadius: '4px',
                fontSize: '11px',
                fontFamily: 'monospace',
                fontWeight: 600,
                outline: 'none',
                cursor: 'pointer'
              }}
            >
              {wealthVectors.map((vector, idx) => (
                <option key={idx} value={vector} style={{ backgroundColor: 'var(--bg-panel)', color: 'var(--text-main)' }}>
                  {vector}
                </option>
              ))}
            </select>
          )}
          {activeModule === 'self_evolution' && (
            <select
              value={activeResearchVector}
              onChange={handleResearchVectorChange}
              style={{
                marginLeft: '12px',
                backgroundColor: 'rgba(239, 68, 68, 0.08)',
                border: '1px solid rgba(239, 68, 68, 0.25)',
                color: 'var(--accent-red)',
                padding: '4px 8px',
                borderRadius: '4px',
                fontSize: '11px',
                fontFamily: 'monospace',
                fontWeight: 600,
                outline: 'none',
                cursor: 'pointer'
              }}
            >
              {researchVectors.map((vector, idx) => (
                <option key={idx} value={vector} style={{ backgroundColor: 'var(--bg-panel)', color: 'var(--text-main)' }}>
                  {vector}
                </option>
              ))}
            </select>
          )}

          {/* Quick Access Media Buttons */}
          <div style={{ marginLeft: '12px', display: 'flex', gap: '8px' }}>
            {activeModule === 'tax_finance' && (
              <button
                onClick={() => openFolder('C:\\Users\\Curtis\\Desktop\\PDF Bills')}
                style={{
                  display: 'flex', alignItems: 'center', gap: '4px',
                  backgroundColor: 'rgba(234, 179, 8, 0.1)',
                  border: '1px solid rgba(234, 179, 8, 0.3)',
                  color: 'var(--accent-yellow)', padding: '4px 8px',
                  borderRadius: '4px', fontSize: '11px', fontFamily: 'monospace',
                  cursor: 'pointer', transition: 'all 0.2s ease'
                }}
                onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = 'rgba(234, 179, 8, 0.2)'; }}
                onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = 'rgba(234, 179, 8, 0.1)'; }}
              >
                <Folder size={12} />
                PDF Bills
              </button>
            )}

            {activeModule === 'site_super' && (
              <button
                onClick={() => openFolder('C:\\Users\\Curtis\\Desktop\\work')}
                style={{
                  display: 'flex', alignItems: 'center', gap: '4px',
                  backgroundColor: 'rgba(0, 212, 255, 0.1)',
                  border: '1px solid rgba(0, 212, 255, 0.3)',
                  color: 'var(--accent-blue)', padding: '4px 8px',
                  borderRadius: '4px', fontSize: '11px', fontFamily: 'monospace',
                  cursor: 'pointer', transition: 'all 0.2s ease'
                }}
                onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = 'rgba(0, 212, 255, 0.2)'; }}
                onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = 'rgba(0, 212, 255, 0.1)'; }}
              >
                <Folder size={12} />
                Job Sites (Work)
              </button>
            )}

            {activeModule === 'recomposition' && (
              <>
                {[
                  { name: 'Sounds', path: 'C:\\Users\\Curtis\\Desktop\\sounds' },
                  { name: 'Canvas', path: 'C:\\Users\\Curtis\\Desktop\\Canvas' },
                  { name: 'New Songs', path: 'C:\\Users\\Curtis\\Desktop\\New Songs' },
                  { name: 'Ready for Two Lost', path: 'C:\\Users\\Curtis\\Desktop\\ready for toolost' },
                  { name: 'Music Match', path: 'C:\\Users\\Curtis\\Desktop\\musicmacth' },
                  { name: 'Completed Albums', path: 'C:\\Users\\Curtis\\Desktop\\Completed Albums' },
                  { name: 'Production', path: 'C:\\Users\\Curtis\\Desktop\\Production' }
                ].map(folder => (
                  <button
                    key={folder.name}
                    onClick={() => openFolder(folder.path)}
                    style={{
                      display: 'flex', alignItems: 'center', gap: '4px',
                      backgroundColor: 'rgba(168, 85, 247, 0.1)',
                      border: '1px solid rgba(168, 85, 247, 0.3)',
                      color: 'var(--accent-purple)', padding: '4px 8px',
                      borderRadius: '4px', fontSize: '11px', fontFamily: 'monospace',
                      cursor: 'pointer', transition: 'all 0.2s ease',
                      whiteSpace: 'nowrap'
                    }}
                    onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = 'rgba(168, 85, 247, 0.2)'; }}
                    onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = 'rgba(168, 85, 247, 0.1)'; }}
                  >
                    <Folder size={12} />
                    {folder.name}
                  </button>
                ))}
              </>
            )}

            {(activeModule === 'possibilities' || activeModule === 'protocols') && (
              <button
                onClick={() => openFolder(activeModule === 'possibilities' ? 'C:\\Users\\Curtis\\Desktop\\Keystone Possibilities' : 'C:\\Users\\Curtis\\Desktop\\Keystone Protocols')}
                style={{
                  display: 'flex', alignItems: 'center', gap: '4px',
                  backgroundColor: 'rgba(59, 130, 246, 0.1)',
                  border: '1px solid rgba(59, 130, 246, 0.3)',
                  color: 'var(--accent-blue)', padding: '4px 8px',
                  borderRadius: '4px', fontSize: '11px', fontFamily: 'monospace',
                  cursor: 'pointer', transition: 'all 0.2s ease'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.backgroundColor = 'rgba(59, 130, 246, 0.2)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.backgroundColor = 'rgba(59, 130, 246, 0.1)';
                }}
              >
                <Folder size={12} />
                {activeModule === 'possibilities' ? 'Keystone Possibilities' : 'Keystone Protocols'}
              </button>
            )}
            
            <button
              onClick={() => openFolder('C:\\Users\\Curtis\\Downloads')}
              style={{
                display: 'flex', alignItems: 'center', gap: '4px',
                backgroundColor: 'rgba(107, 114, 128, 0.1)',
                border: '1px solid rgba(107, 114, 128, 0.3)',
                color: 'var(--text-muted)', padding: '4px 8px',
                borderRadius: '4px', fontSize: '11px', fontFamily: 'monospace',
                cursor: 'pointer', transition: 'all 0.2s ease'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = 'rgba(107, 114, 128, 0.2)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'rgba(107, 114, 128, 0.1)';
              }}
            >
              <Folder size={12} />
              Downloads
            </button>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <button 
            className="commit-learning-btn"
            disabled={isCommittingLearning}
            onClick={handleCommitLearningAuto}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              backgroundColor: committedRuleId 
                ? 'rgba(16, 185, 129, 0.15)' 
                : commitError 
                ? 'rgba(239, 68, 68, 0.15)' 
                : 'rgba(251, 191, 36, 0.08)',
              border: committedRuleId 
                ? '1px solid #10b981' 
                : commitError 
                ? '1px solid #ef4444' 
                : '1px solid var(--accent-gold)',
              color: committedRuleId 
                ? '#10b981' 
                : commitError 
                ? '#f87171' 
                : 'var(--accent-gold)',
              padding: '6px 12px',
              borderRadius: '6px',
              fontSize: '11px',
              fontWeight: 600,
              cursor: isCommittingLearning ? 'not-allowed' : 'pointer',
              transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
              fontFamily: 'monospace'
            }}
          >
            <Sparkles size={12} />
            <span>
              {isCommittingLearning 
                ? 'COMMITTING...' 
                : committedRuleId 
                ? `COMMITTED: ${committedRuleId}` 
                : commitError 
                ? commitError 
                : 'COMMIT LEARNING'}
            </span>
          </button>

          <button 
            className="sync-drive-btn"
            disabled={isSyncingDrive}
            onClick={handleSyncDrive}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              backgroundColor: syncStatus === 'synced'
                ? 'rgba(16, 185, 129, 0.15)' 
                : syncStatus === 'failed'
                ? 'rgba(239, 68, 68, 0.15)' 
                : 'rgba(59, 130, 246, 0.08)',
              border: syncStatus === 'synced'
                ? '1px solid #10b981' 
                : syncStatus === 'failed'
                ? '1px solid #ef4444' 
                : '1px solid var(--accent-blue)',
              color: syncStatus === 'synced'
                ? '#10b981' 
                : syncStatus === 'failed'
                ? '#f87171' 
                : 'var(--accent-blue)',
              padding: '6px 12px',
              borderRadius: '6px',
              fontSize: '11px',
              fontWeight: 600,
              cursor: isSyncingDrive ? 'not-allowed' : 'pointer',
              transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
              fontFamily: 'monospace'
            }}
          >
            <RefreshCw size={12} className={isSyncingDrive ? "spin-animation" : ""} />
            <span>
              {isSyncingDrive 
                ? 'SYNCING...' 
                : syncStatus === 'synced' 
                ? 'SYNC COMPLETE' 
                : syncStatus === 'failed' 
                ? 'SYNC FAILED' 
                : 'SYNC SPARK & NOTEBOOK'}
            </span>
          </button>
          
          {!isArchiveOpen && (
            <PanelRightOpen 
              size={18} 
              color="var(--text-muted)" 
              style={{ cursor: 'pointer' }} 
              onClick={onOpenArchive} 
            />
          )}
        </div>
      </div>

      {/* Tab Selector Bar */}
      <div style={{
        display: 'flex',
        backgroundColor: 'rgba(0, 0, 0, 0.15)',
        borderBottom: '1px solid var(--border-color)',
        padding: '0 16px',
        height: '36px',
        alignItems: 'center',
        gap: '24px',
        flexShrink: 0
      }}>
        {[
          { id: 'chat', label: 'ACTIVE SESSION' },
          { id: 'bootstrap', label: 'MODULE BOOTSTRAP' }
        ].map(tab => {
          const isActive = activeTab === tab.id;
          return (
            <div
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              style={{
                fontSize: '10px',
                fontWeight: 600,
                letterSpacing: '1px',
                fontFamily: 'monospace',
                cursor: 'pointer',
                padding: '10px 4px',
                color: isActive ? 'var(--accent-gold)' : 'var(--text-muted)',
                borderBottom: isActive ? '2px solid var(--accent-gold)' : '2px solid transparent',
                transition: 'all 0.2s ease',
                height: '100%',
                display: 'flex',
                alignItems: 'center'
              }}
              onMouseEnter={(e) => {
                if (!isActive) e.currentTarget.style.color = '#00d4ff';
              }}
              onMouseLeave={(e) => {
                if (!isActive) e.currentTarget.style.color = 'var(--text-muted)';
              }}
            >
              {tab.label}
            </div>
          );
        })}
      </div>

      {/* Tab Contents */}
      {activeTab === 'chat' && (
        <>
          {/* Chat Feed */}
          <div 
            ref={scrollContainerRef}
            style={{ flex: 1, padding: '24px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '16px' }}
          >
            {messages.length === 0 ? (
              <div style={{ margin: 'auto', color: 'var(--text-muted)', fontSize: '14px', fontFamily: 'monospace' }}>
                A.I.D.A. SYSTEM ONLINE. AWAITING INPUT...
              </div>
            ) : (
              messages.map((msg, index) => (
                <div key={index} style={{
                  backgroundColor: msg.sender === 'user' ? 'rgba(0, 212, 255, 0.03)' : 'var(--bg-panel)',
                  padding: '16px',
                  borderRadius: '8px',
                  border: msg.sender === 'user' ? '1px solid rgba(0, 212, 255, 0.15)' : '1px solid var(--border-color)',
                  alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                  marginLeft: msg.sender === 'user' ? '1in' : '0',
                  marginRight: msg.sender === 'user' ? '0' : '1in',
                  width: msg.sender === 'user' ? 'calc(100% - 1in)' : 'auto',
                  maxWidth: 'calc(100% - 1in)',
                  boxShadow: '0 2px 8px rgba(0, 0, 0, 0.15)',
                  whiteSpace: 'pre-wrap',
                  wordBreak: 'break-word'
                }}>
                  <div style={{
                    fontSize: '11px',
                    fontWeight: 700,
                    color: msg.sender === 'user' ? 'var(--accent-blue)' : 'var(--accent-green)',
                    fontFamily: 'monospace',
                    marginBottom: '8px',
                    letterSpacing: '0.5px'
                  }}>
                    {msg.sender === 'user' ? 'USER' : 'A.I.D.A. SYSTEM'}
                  </div>
                  <MarkdownRenderer content={msg.text} onLinkClick={onOpenFile} />
                  
                  {/* File Changes Widget */}
                  {msg.file_changes && msg.file_changes.length > 0 && (
                    <div style={{
                      marginTop: '12px',
                      padding: '10px 14px',
                      borderRadius: '6px',
                      backgroundColor: 'rgba(0, 0, 0, 0.2)',
                      border: '1px solid var(--border-color)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      gap: '12px'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '11px', fontFamily: 'monospace' }}>
                        <span style={{ color: 'var(--text-main)' }}>
                          {msg.file_changes.length} file{msg.file_changes.length > 1 ? 's' : ''} changed
                        </span>
                        {(() => {
                          const totalAdd = msg.file_changes.reduce((sum, f) => sum + f.additions, 0);
                          const totalDel = msg.file_changes.reduce((sum, f) => sum + f.deletions, 0);
                          return (
                            <>
                              {totalAdd > 0 && (
                                <span style={{ color: 'var(--accent-green)', fontWeight: 600 }}>+{totalAdd}</span>
                              )}
                              {totalDel > 0 && (
                                <span style={{ color: 'var(--accent-red)', fontWeight: 600 }}>-{totalDel}</span>
                              )}
                            </>
                          );
                        })()}
                      </div>
                      
                      <button
                        onClick={() => {
                          if (onOpenFile && msg.file_changes[0]) {
                            onOpenFile(msg.file_changes[0].path);
                          }
                        }}
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '6px',
                          backgroundColor: 'rgba(255, 255, 255, 0.03)',
                          border: '1px solid var(--border-color)',
                          color: 'var(--text-main)',
                          padding: '4px 10px',
                          borderRadius: '4px',
                          fontSize: '11px',
                          cursor: 'pointer',
                          fontFamily: 'monospace',
                          transition: 'all 0.2s ease'
                        }}
                        onMouseEnter={(e) => {
                          e.currentTarget.style.borderColor = 'var(--accent-blue)';
                          e.currentTarget.style.backgroundColor = 'rgba(0, 212, 255, 0.05)';
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.borderColor = 'var(--border-color)';
                          e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.03)';
                        }}
                      >
                        <FileText size={12} color="var(--accent-blue)" />
                        <span>Review</span>
                      </button>
                    </div>
                  )}
                </div>
              ))
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Footer */}
          <div style={{ padding: '16px', borderTop: '1px solid var(--border-color)' }}>
            
            {/* Real-time Status Indicators Bar */}
            {(() => {
              const isChatGenerating = messages.length > 0 && (
                messages[messages.length - 1].sender === 'user' ||
                messages[messages.length - 1].is_thinking
              );
              const isVoiceActive = voiceState === 'listening' || voiceState === 'speaking';

              return (
                <>
                  <style dangerouslySetInnerHTML={{__html: `
                    @keyframes dot-blink {
                      0% { opacity: 0.3; }
                      20% { opacity: 1; }
                      100% { opacity: 0.3; }
                    }
                    @keyframes border-pulse {
                      0% { border-color: rgba(0, 212, 255, 0.1); box-shadow: 0 0 4px rgba(0, 212, 255, 0.02); }
                      50% { border-color: rgba(0, 212, 255, 0.22); box-shadow: 0 0 10px rgba(0, 212, 255, 0.08); }
                      100% { border-color: rgba(0, 212, 255, 0.1); box-shadow: 0 0 4px rgba(0, 212, 255, 0.02); }
                    }
                  `}} />
                  <div style={{
                    backgroundColor: 'rgba(10, 15, 30, 0.65)',
                    padding: '8px 16px',
                    borderRadius: '6px',
                    border: '1px solid rgba(0, 212, 255, 0.12)',
                    width: '100%',
                    margin: '0 0 12px 0',
                    boxShadow: '0 4px 16px rgba(0, 0, 0, 0.4)',
                    display: 'flex',
                    flexDirection: 'row',
                    alignItems: 'center',
                    justifyContent: 'flex-start',
                    gap: '20px',
                    animation: 'border-pulse 3.0s ease-in-out infinite',
                    backdropFilter: 'blur(10px)',
                    alignSelf: 'center',
                    flexWrap: 'wrap'
                  }}>
                    <span style={{ fontSize: '9px', fontFamily: 'monospace', color: 'var(--text-muted)', fontWeight: 600, letterSpacing: '1px', textTransform: 'uppercase', borderRight: '1px solid rgba(255,255,255,0.08)', paddingRight: '14px', marginRight: '-6px' }}>
                      Status
                    </span>

                    {/* Channel 1: Voice Bridge */}
                    {isVoiceActive ? (
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', opacity: 1, transition: 'all 0.3s ease' }}>
                        <div style={{ display: 'flex', gap: '2px' }}>
                          <span style={{ width: '4px', height: '4px', borderRadius: '50%', backgroundColor: voiceState === 'listening' ? '#00ffaa' : '#00d4ff', display: 'inline-block', animation: 'dot-blink 1.4s infinite both' }} />
                          <span style={{ width: '4px', height: '4px', borderRadius: '50%', backgroundColor: voiceState === 'listening' ? '#00ffaa' : '#00d4ff', display: 'inline-block', animation: 'dot-blink 1.4s infinite both 0.2s' }} />
                        </div>
                        <span style={{ fontSize: '10.5px', fontFamily: 'monospace', color: voiceState === 'listening' ? '#00ffaa' : '#00d4ff', fontWeight: 600, letterSpacing: '0.3px', textShadow: voiceState === 'listening' ? '0 0 6px rgba(0, 255, 170, 0.4)' : '0 0 6px rgba(0, 212, 255, 0.4)' }}>
                          [VOICE BRIDGE] {voiceState === 'listening' ? 'listening' : 'speaking'}
                        </span>
                      </div>
                    ) : (
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', opacity: 0.35, transition: 'all 0.3s ease' }}>
                        <span style={{ width: '4px', height: '4px', borderRadius: '50%', backgroundColor: 'var(--text-muted)', display: 'inline-block' }} />
                        <span style={{ fontSize: '10.5px', fontFamily: 'monospace', color: 'var(--text-muted)', fontWeight: 500, letterSpacing: '0.3px' }}>
                          [VOICE BRIDGE] standby
                        </span>
                      </div>
                    )}

                    {/* Channel 2: Agent Fleet */}
                    {isAgentWorking ? (
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', opacity: 1, transition: 'all 0.3s ease' }}>
                        <div style={{ display: 'flex', gap: '2px' }}>
                          <span style={{ width: '4px', height: '4px', borderRadius: '50%', backgroundColor: '#00d4ff', display: 'inline-block', animation: 'dot-blink 1.4s infinite both' }} />
                          <span style={{ width: '4px', height: '4px', borderRadius: '50%', backgroundColor: '#00d4ff', display: 'inline-block', animation: 'dot-blink 1.4s infinite both 0.2s' }} />
                        </div>
                        <span style={{ fontSize: '10.5px', fontFamily: 'monospace', color: '#00d4ff', fontWeight: 600, letterSpacing: '0.3px', textShadow: '0 0 6px rgba(0, 212, 255, 0.4)' }}>
                          [AGENT FLEET] working ({activeAgentsCount} active)
                        </span>
                      </div>
                    ) : (
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', opacity: 0.35, transition: 'all 0.3s ease' }}>
                        <span style={{ width: '4px', height: '4px', borderRadius: '50%', backgroundColor: 'var(--text-muted)', display: 'inline-block' }} />
                        <span style={{ fontSize: '10.5px', fontFamily: 'monospace', color: 'var(--text-muted)', fontWeight: 500, letterSpacing: '0.3px' }}>
                          [AGENT FLEET] standby
                        </span>
                      </div>
                    )}

                    {/* Channel 3: Python (Pantheon) */}
                    {isPythonWorking ? (
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', opacity: 1, transition: 'all 0.3s ease' }}>
                        <div style={{ display: 'flex', gap: '2px' }}>
                          <span style={{ width: '4px', height: '4px', borderRadius: '50%', backgroundColor: '#ffaa00', display: 'inline-block', animation: 'dot-blink 1.4s infinite both' }} />
                          <span style={{ width: '4px', height: '4px', borderRadius: '50%', backgroundColor: '#ffaa00', display: 'inline-block', animation: 'dot-blink 1.4s infinite both 0.2s' }} />
                        </div>
                        <span style={{ fontSize: '10.5px', fontFamily: 'monospace', color: '#ffaa00', fontWeight: 600, letterSpacing: '0.3px', textShadow: '0 0 6px rgba(255, 170, 0, 0.4)' }}>
                          [PYTHON TASK] active ({activePythonTasksCount} active)
                        </span>
                      </div>
                    ) : (
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', opacity: 0.35, transition: 'all 0.3s ease' }}>
                        <span style={{ width: '4px', height: '4px', borderRadius: '50%', backgroundColor: 'var(--text-muted)', display: 'inline-block' }} />
                        <span style={{ fontSize: '10.5px', fontFamily: 'monospace', color: 'var(--text-muted)', fontWeight: 500, letterSpacing: '0.3px' }}>
                          [PYTHON TASK] standby
                        </span>
                      </div>
                    )}

                    {/* Channel 4: Chat Generator */}
                    {isChatGenerating ? (
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', opacity: 1, transition: 'all 0.3s ease' }}>
                        <div style={{ display: 'flex', gap: '2px' }}>
                          <span style={{ width: '4px', height: '4px', borderRadius: '50%', backgroundColor: '#d946ef', display: 'inline-block', animation: 'dot-blink 1.4s infinite both' }} />
                          <span style={{ width: '4px', height: '4px', borderRadius: '50%', backgroundColor: '#d946ef', display: 'inline-block', animation: 'dot-blink 1.4s infinite both 0.2s' }} />
                        </div>
                        <span style={{ fontSize: '10.5px', fontFamily: 'monospace', color: '#d946ef', fontWeight: 600, letterSpacing: '0.3px', textShadow: '0 0 6px rgba(217, 70, 239, 0.4)' }}>
                          [CHAT PROCESS] processing
                        </span>
                      </div>
                    ) : (
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', opacity: 0.35, transition: 'all 0.3s ease' }}>
                        <span style={{ width: '4px', height: '4px', borderRadius: '50%', backgroundColor: 'var(--text-muted)', display: 'inline-block' }} />
                        <span style={{ fontSize: '10.5px', fontFamily: 'monospace', color: 'var(--text-muted)', fontWeight: 500, letterSpacing: '0.3px' }}>
                          [CHAT PROCESS] standby
                        </span>
                      </div>
                    )}
                  </div>
                </>
              );
            })()}

            {/* Staged Uploaded Files */}
            {uploadedFiles.length > 0 && (
              <div style={{
                display: 'flex',
                flexWrap: 'wrap',
                gap: '8px',
                marginBottom: '10px',
                padding: '4px'
              }}>
                {uploadedFiles.map((file, idx) => (
                  <div key={idx} style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                    backgroundColor: 'rgba(0, 212, 255, 0.08)',
                    border: '1px solid rgba(0, 212, 255, 0.25)',
                    color: 'var(--accent-blue)',
                    padding: '4px 8px',
                    borderRadius: '4px',
                    fontSize: '11px',
                    fontFamily: 'monospace'
                  }}>
                    <FileText size={12} color="var(--accent-blue)" />
                    <span style={{ maxWidth: '180px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }} title={file.name}>
                      {file.name}
                    </span>
                    <span 
                      onClick={() => setUploadedFiles(uploadedFiles.filter((_, i) => i !== idx))}
                      style={{
                        cursor: 'pointer',
                        fontWeight: 'bold',
                        marginLeft: '4px',
                        color: 'var(--text-muted)'
                      }}
                      onMouseEnter={(e) => e.currentTarget.style.color = 'var(--accent-red)'}
                      onMouseLeave={(e) => e.currentTarget.style.color = 'var(--text-muted)'}
                    >
                      ✕
                    </span>
                  </div>
                ))}
              </div>
            )}

            <div style={{
              display: 'flex',
              alignItems: 'center',
              backgroundColor: 'var(--bg-panel)',
              border: '1px solid var(--border-color)',
              borderRadius: '8px',
              padding: '8px 12px',
              gap: '12px'
            }}>
              <input 
                type="file" 
                ref={fileInputRef} 
                style={{ display: 'none' }} 
                multiple 
                onChange={handleFileChange} 
              />
              <Paperclip 
                size={18} 
                color="var(--text-muted)" 
                style={{cursor: 'pointer'}} 
                onClick={() => fileInputRef.current?.click()}
              />
              <input 
                type="text" 
                placeholder={isLocalListening ? "Listening... Speak now..." : "Type a command or drop documentation here..."} 
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyDown={handleInputKeyDown}
                style={{
                  flex: 1,
                  background: 'transparent',
                  border: 'none',
                  color: 'var(--text-main)',
                  outline: 'none',
                  fontSize: '14.5px'
                }}
              />
              <Mic 
                size={18} 
                color={
                  isLocalListening || voiceState === 'listening' ? 'var(--accent-red)' :
                  voiceState === 'speaking' ? 'var(--accent-green)' :
                  voiceBridgeStatus === 'connected' ? 'var(--accent-blue)' :
                  'var(--text-muted)'
                } 
                style={{
                  cursor: 'pointer',
                  filter: isLocalListening || voiceState === 'listening' ? 'drop-shadow(0 0 4px var(--accent-red))' : 'none',
                  transition: 'all 0.2s ease'
                }} 
                onMouseDown={startLocalListening}
                onMouseUp={() => stopLocalListening(true)}
                onTouchStart={(e) => { e.preventDefault(); startLocalListening(); }}
                onTouchEnd={(e) => { e.preventDefault(); stopLocalListening(true); }}
              />
              <div 
                onClick={handleSubmit}
                style={{
                  background: 'var(--accent-blue)',
                  borderRadius: '4px',
                  padding: '6px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  cursor: 'pointer'
                }}
              >
                <Send size={14} color="#fff" />
              </div>
            </div>
          </div>
        </>
      )}

      {activeTab === 'bootstrap' && (
        <div style={{ flex: 1, padding: '24px', overflowY: 'auto', display: 'flex', flexDirection: 'column' }}>
          <div style={{ 
            backgroundColor: 'var(--bg-panel)', 
            padding: '24px', 
            borderRadius: '8px', 
            border: '1px solid var(--border-color)',
            flex: 1,
            overflowY: 'auto'
          }}>
            <MarkdownRenderer content={bootstrapText} onLinkClick={onOpenFile} />
          </div>
        </div>
      )}

    </div>
  );
};

export default ChatArea;
