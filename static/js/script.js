let allComments = [];
        let currentFilter = 'all';
        
        // Load users on start
        async function loadUsers() {
            try {
                const response = await fetch('/api/users');
                const data = await response.json();
                const select = document.getElementById('userId');
                select.innerHTML = '<option value="">-- Seleccionar Usuario --</option>';
                data.users.forEach(user => {
                    select.innerHTML += `<option value="${user.id}">${user.name} (${user.email})</option>`;
                });
                document.getElementById('totalUsers').textContent = data.users.length;
            } catch (error) {
                console.error('Error loading users:', error);
            }
        }
        
        // Load comments
        async function loadComments() {
            try {
                const response = await fetch('/api/comments');
                const data = await response.json();
                allComments = data.comments;
                
                updateStatistics();
                displayComments();
            } catch (error) {
                console.error('Error loading comments:', error);
            }
        }
        
        // Update statistics
        function updateStatistics() {
            const total = allComments.length;
            document.getElementById('totalComments').textContent = total;
            
            if (total === 0) {
                document.getElementById('avgConfidence').textContent = '0%';
                document.getElementById('positivePercent').textContent = '0%';
                return;
            }
            
            const avgConf = allComments.reduce((sum, c) => sum + c.confidence, 0) / total;
            document.getElementById('avgConfidence').textContent = avgConf.toFixed(1) + '%';
            
            const positives = allComments.filter(c => c.sentiment.toLowerCase() === 'positive').length;
            const positivePercent = (positives / total * 100).toFixed(0);
            document.getElementById('positivePercent').textContent = positivePercent + '%';
        }
        
        // Display comments
        function displayComments() {
            const container = document.getElementById('commentsList');
            
            let commentsToShow = allComments;
            if (currentFilter !== 'all') {
                commentsToShow = allComments.filter(c => c.sentiment.toLowerCase() === currentFilter);
            }
            
            if (commentsToShow.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">📭</div>
                        <h3>No hay comentarios aún</h3>
                        <p>Crea tu primer comentario para empezar</p>
                    </div>
                `;
                return;
            }
            
            container.innerHTML = commentsToShow.map(c => {
                const sentimentEmoji = {
                    'positive': '😊',
                    'negative': '😞',
                    'neutral': '😐'
                }[c.sentiment.toLowerCase()] || '😐';
                
                return `
                    <div class="comment-item">
                        <div class="comment-header">
                            <div>
                                <div class="comment-user">${c.user.name}</div>
                                <div class="comment-email">${c.user.email}</div>
                            </div>
                        </div>
                        <div class="comment-text">${c.text}</div>
                        <div class="comment-meta">
                            <span class="sentiment-badge sentiment-${c.sentiment}">
                                ${sentimentEmoji} ${c.sentiment.toUpperCase()}
                            </span>
                            <div class="confidence">
                                <span>🎯 ${c.confidence}%</span>
                                <div class="confidence-bar">
                                    <div class="confidence-fill" style="width: ${c.confidence}%"></div>
                                </div>
                            </div>
                            <span class="comment-date">📅 ${new Date(c.analysis_date).toLocaleString('es-ES')}</span>
                        </div>
                    </div>
                `;
            }).join('');
        }
        
        // Filter comments
        function filterComments(sentiment) {
            currentFilter = sentiment;
            displayComments();
        }
        
        // Quick analysis
        async function quickAnalysis() {
            const input = document.getElementById('quickTestInput');
            const resultDiv = document.getElementById('quickResult');
            const text = input.value.trim();
            
            if (!text) {
                resultDiv.innerHTML = '<div class="alert alert-error">⚠️ Escribe un texto para analizar</div>';
                return;
            }
            
            resultDiv.innerHTML = '<div style="text-align:center"><div class="loading"></div></div>';
            
            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: text})
                });
                
                const data = await response.json();
                
                const sentimentEmoji = {
                    'positive': '😊',
                    'negative': '😞',
                    'neutral': '😐'
                }[data.sentiment.toLowerCase()] || '😐';
                
                resultDiv.innerHTML = `
                    <div class="quick-result">
                        <h4 style="margin-bottom: 10px;">Resultado:</h4>
                        <div style="font-size: 2em; margin: 10px 0;">${sentimentEmoji}</div>
                        <div style="font-size: 1.3em; font-weight: bold; margin-bottom: 5px;">
                            ${data.sentiment.toUpperCase()}
                        </div>
                        <div>Confianza: ${data.confidence}%</div>
                    </div>
                `;
            } catch (error) {
                resultDiv.innerHTML = '<div class="alert alert-error">❌ Error al analizar</div>';
            }
        }
        
        // Register user
        document.getElementById('userForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const alertDiv = document.getElementById('userAlert');
            
            try {
                const response = await fetch('/api/users', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        name: document.getElementById('userName').value,
                        email: document.getElementById('userEmail').value
                    })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    alertDiv.innerHTML = '<div class="alert alert-success">✅ Usuario registrado exitosamente</div>';
                    e.target.reset();
                    loadUsers();
                } else {
                    alertDiv.innerHTML = `<div class="alert alert-error">❌ ${data.error}</div>`;
                }
            } catch (error) {
                alertDiv.innerHTML = '<div class="alert alert-error">❌ Error al registrar usuario</div>';
            }
            
            setTimeout(() => alertDiv.innerHTML = '', 4000);
        });
        
        // Create comment
        document.getElementById('commentForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const alertDiv = document.getElementById('commentAlert');
            const button = e.target.querySelector('button');
            const originalText = button.innerHTML;
            
            button.innerHTML = '<div class="loading"></div> Analizando...';
            button.disabled = true;
            
            try {
                const response = await fetch('/api/comments', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        user_id: document.getElementById('userId').value,
                        text: document.getElementById('commentText').value
                    })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    const sentiment = data.analysis.sentiment;
                    const confidence = data.analysis.confidence;
                    const emojiList = {
                        'positive': '😊',
                        'negative': '😞',
                        'neutral': '😐'
                    };
                    
                    alertDiv.innerHTML = `
                        <div class="alert alert-success">
                            ✅ Comentario analizado: <strong>${emojiList[sentiment.toLowerCase()]} ${sentiment.toUpperCase()}</strong> 
                            (Confianza: ${confidence}%)
                        </div>
                    `;
                    e.target.reset();
                    loadComments();
                } else {
                    alertDiv.innerHTML = `<div class="alert alert-error">❌ ${data.error}</div>`;
                }
            } catch (error) {
                alertDiv.innerHTML = '<div class="alert alert-error">❌ Error al crear comentario</div>';
            } finally {
                button.innerHTML = originalText;
                button.disabled = false;
            }
            
            setTimeout(() => alertDiv.innerHTML = '', 5000);
        });
        
        // Quick test on Enter
        document.getElementById('quickTestInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                quickAnalysis();
            }
        });
        
        // Initialize
        loadUsers();
        loadComments();
        
        // Auto-refresh every 10 seconds
        setInterval(() => {
            loadComments();
        }, 10000);