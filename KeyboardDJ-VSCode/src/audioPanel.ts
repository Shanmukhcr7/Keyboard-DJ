import * as vscode from 'vscode';

export class AudioPanel {
    public static currentPanel: AudioPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private _disposables: vscode.Disposable[] = [];

    private constructor(panel: vscode.WebviewPanel, extensionUri: vscode.Uri) {
        this._panel = panel;
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
        this._panel.webview.html = this._getHtmlForWebview(this._panel.webview, extensionUri);
    }

    public static createOrShow(extensionUri: vscode.Uri) {
        if (AudioPanel.currentPanel) {
            // Already showing
            return;
        }

        const panel = vscode.window.createWebviewPanel(
            'keyboardDjAudio',
            'Keyboard DJ Audio Engine',
            vscode.ViewColumn.Beside, // We can optionally hide it or keep it in a small tab
            {
                enableScripts: true,
                retainContextWhenHidden: true // Keep audio playing when tab is hidden!
            }
        );

        AudioPanel.currentPanel = new AudioPanel(panel, extensionUri);
    }

    public static kill() {
        AudioPanel.currentPanel?.dispose();
        AudioPanel.currentPanel = undefined;
    }

    public playMusic() {
        this._panel.webview.postMessage({ command: 'play' });
    }

    public pauseMusic() {
        this._panel.webview.postMessage({ command: 'pause' });
    }

    public dispose() {
        AudioPanel.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const x = this._disposables.pop();
            if (x) {
                x.dispose();
            }
        }
    }

    private _getHtmlForWebview(webview: vscode.Webview, extensionUri: vscode.Uri) {
        // Path to the HTML file
        const htmlPath = vscode.Uri.joinPath(extensionUri, 'media', 'audio.html');
        // We can inject the actual URI of the audio file to the HTML
        const audioUri = webview.asWebviewUri(vscode.Uri.joinPath(extensionUri, 'media', 'music', 'lofi.mp3'));

        return `<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Keyboard DJ Audio</title>
        </head>
        <body style="background: #1e1e1e; color: white; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; flex-direction: column;">
            <h2>🎵 Keyboard DJ Engine Running</h2>
            <p>You can close or hide this tab. Audio runs in the background.</p>
            <audio id="bg-audio" src="${audioUri}" loop></audio>

            <script>
                const audio = document.getElementById('bg-audio');
                audio.volume = 0.5;

                window.addEventListener('message', event => {
                    const message = event.data;
                    switch (message.command) {
                        case 'play':
                            audio.play().catch(e => console.error("Audio play failed:", e));
                            break;
                        case 'pause':
                            audio.pause();
                            break;
                    }
                });
            </script>
        </body>
        </html>`;
    }
}
