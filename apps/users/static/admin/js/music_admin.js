// Script para melhorar o upload de músicas no admin
(function() {
    'use strict';
    
    document.addEventListener('DOMContentLoaded', function() {
        const fileInput = document.querySelector('#id_file');
        
        if (fileInput) {
            // Adicionar indicador visual ao campo de arquivo
            const fileField = fileInput.closest('.form-row');
            if (fileField && !document.querySelector('.music-upload-help')) {
                const helpText = document.createElement('div');
                helpText.className = 'music-upload-help';
                helpText.innerHTML = `
                    <p>
                        📌 <strong>Limite:</strong> 500MB por arquivo<br>
                        ⏳ <strong>Processamento:</strong> Arquivos grandes podem demorar alguns minutos
                    </p>
                `;
                fileField.appendChild(helpText);
            }
            
            // Mostrar indicador quando arquivo for selecionado
            fileInput.addEventListener('change', function(e) {
                if (e.target.files && e.target.files.length > 0) {
                    const file = e.target.files[0];
                    const fileSizeMB = (file.size / 1024 / 1024).toFixed(2);
                    
                    // Remover indicador anterior se existir
                    let oldProgress = document.querySelector('.music-upload-progress');
                    if (oldProgress) oldProgress.remove();
                    
                    // Criar novo indicador de progresso
                    const progressBar = document.createElement('div');
                    progressBar.className = 'music-upload-progress';
                    progressBar.innerHTML = `
                        <p><strong>⏳ Upload em progresso...</strong></p>
                        <p>📁 Arquivo: <strong>${file.name}</strong> (${fileSizeMB}MB)</p>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: 100%;"></div>
                        </div>
                        <p style="margin-top: 12px; font-size: 13px; color: #6b7280;">
                            🔄 Por favor, aguarde... não feche esta página.
                        </p>
                    `;
                    fileField.appendChild(progressBar);
                    progressBar.classList.add('active');
                }
            });
            
            // Mostrar aviso crítico no submit
            const form = fileInput.closest('form');
            if (form) {
                form.addEventListener('submit', function() {
                    const progressBar = document.querySelector('.music-upload-progress');
                    if (progressBar && fileInput.files.length > 0) {
                        progressBar.innerHTML = `
                            <p class="warning-msg">⚠️ CRÍTICO: NÃO FECHE ESTA PÁGINA!</p>
                            <p><strong>⏳ Upload em progresso...</strong></p>
                            <p>📁 Arquivo: <strong>${fileInput.files[0].name}</strong></p>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: 100%;"></div>
                            </div>
                            <p style="margin-top: 12px; color: #dc2626; font-weight: 600;">
                                ❌ Fechar agora pode corromper o arquivo!
                            </p>
                        `;
                        progressBar.classList.add('active');
                    }
                });
            }
        }
    });
})();
