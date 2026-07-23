"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = require("vscode");
const audioPanel_1 = require("./audioPanel");
let timeoutId;
let isPlaying = false;
const TIMEOUT_MS = 300; // Pause music after 300ms of no typing
function activate(context) {
    console.log('Keyboard DJ is now active!');
    const startCommand = vscode.commands.registerCommand('keyboard-dj.start', () => {
        audioPanel_1.AudioPanel.createOrShow(context.extensionUri);
        vscode.window.showInformationMessage('Keyboard DJ: Started! Start typing to feel the music 🎶');
    });
    const stopCommand = vscode.commands.registerCommand('keyboard-dj.stop', () => {
        audioPanel_1.AudioPanel.kill();
        vscode.window.showInformationMessage('Keyboard DJ: Stopped.');
    });
    // Listen to keystrokes (changes in text document)
    const onTypeEvent = vscode.workspace.onDidChangeTextDocument((event) => {
        if (!audioPanel_1.AudioPanel.currentPanel)
            return;
        // User typed something
        if (!isPlaying) {
            audioPanel_1.AudioPanel.currentPanel.playMusic();
            isPlaying = true;
        }
        // Reset the inactivity timeout
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        timeoutId = setTimeout(() => {
            if (audioPanel_1.AudioPanel.currentPanel) {
                audioPanel_1.AudioPanel.currentPanel.pauseMusic();
            }
            isPlaying = false;
        }, TIMEOUT_MS);
    });
    context.subscriptions.push(startCommand, stopCommand, onTypeEvent);
}
function deactivate() {
    audioPanel_1.AudioPanel.kill();
}
//# sourceMappingURL=extension.js.map