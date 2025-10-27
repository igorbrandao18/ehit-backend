// Script para melhorar o upload de músicas no admin
(function() {
    'use strict';
    
    document.addEventListener('DOMContentLoaded', function() {
        const fileInput = document.querySelector('#id_file');
        
        if (fileInput) {
            // Adicionar indicador visual ao campo de arquivo
            const fileField = fileInput.closest('.form-row');
            if (fileField) {
                const helpText = document.createElement('div');
                helpText.className = 'music-upload-help';
                helpText.innerHTML = `
                    <p style="color: #856404; background: #fff3cd; padding: 8px; border-left: 3px solid #ffc107; margin-top: 5px;">
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
                    
                    // Adicionar indicador de progresso
                    let progressBar = document.querySelector('.music-upload-progress');
                    if (!progressBar) {
                        progressBar = document.createElement('div');
                        progressBar.className = 'music-upload-progress';
                        progressBar.innerHTML = `
                            <p><strong>⏳ Upload em progresso...</strong></p>
                            <p>Arquivo: ${file.name} (${fileSizeMB}MB)</p>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: 100%;"></div>
                            </div>
                            <p style="margin-top: 10px; color: #666;">
                                Por favor, não feche esta página enquanto o arquivo está sendo processado.
                            </p>
                        `;
                        fileInput.closest('.form-row').appendChild(progressBar);
                    }
                    
                    // Ativar indicador
                    progressBar.classList.add('active');
                }
            });
            
            // Mostrar indicador no submit
            const form = fileInput.closest('form');
            if (form) {
                form.addEventListener('submit', function() {
                    const progressBar = document.querySelector('.music-upload-progress');
                    if (progressBar && fileInput.files.length > 0) {
                        progressBar.classList.add('active');
                        
                        // Adicionar mensagem de não fechar
                        const msg = document.createElement('p');
                        msg.style.cssText = 'background: #f44336; color: white; padding: 15px; margin: 10px 0; border-radius: 5px; text-align: center; font-weight: bold;';
                        msg.textContent = '⚠️ NÃO FECHE ESTA PÁGINA! O upload está em progresso...';
                        if (progressBar.querySelector('.warning-msg')) {
                            progressBar.querySelector('.warning-msg').remove();
                        }
                        msg.className = 'warning-msg';
                        progressBar.insertBefore(msg, progressBar.firstChild);
                    }
                });
            }
        }
    });
})();
