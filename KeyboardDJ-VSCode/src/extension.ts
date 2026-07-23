import * as vscode from 'vscode';
import { AudioPanel } from './audioPanel';

let timeoutId: NodeJS.Timeout | undefined;
let isPlaying = false;
const TIMEOUT_MS = 300; // Pause music after 300ms of no typing

export function activate(context: vscode.ExtensionContext) {
    console.log('Keyboard DJ is now active!');

    const startCommand = vscode.commands.registerCommand('keyboard-dj.start', () => {
        AudioPanel.createOrShow(context.extensionUri);
        vscode.window.showInformationMessage('Keyboard DJ: Started! Start typing to feel the music 🎶');
    });

    const stopCommand = vscode.commands.registerCommand('keyboard-dj.stop', () => {
        AudioPanel.kill();
        vscode.window.showInformationMessage('Keyboard DJ: Stopped.');
    });

    // Listen to keystrokes (changes in text document)
    const onTypeEvent = vscode.workspace.onDidChangeTextDocument((event) => {
        if (!AudioPanel.currentPanel) return;

        // User typed something
        if (!isPlaying) {
            AudioPanel.currentPanel.playMusic();
            isPlaying = true;
        }

        // Reset the inactivity timeout
        if (timeoutId) {
            clearTimeout(timeoutId);
        }

        timeoutId = setTimeout(() => {
            if (AudioPanel.currentPanel) {
                AudioPanel.currentPanel.pauseMusic();
            }
            isPlaying = false;
        }, TIMEOUT_MS);
    });

    context.subscriptions.push(startCommand, stopCommand, onTypeEvent);
}

export function deactivate() {
    AudioPanel.kill();
}
