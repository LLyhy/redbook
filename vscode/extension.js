const vscode = require('vscode');
const https = require('https');
const http = require('http');

const REDBOOK_SYSTEM_PROMPT = `你是红宝书。用矛盾分析法回答算法问题。语录必须对应具体算法，不空喊。

=== 解题 ===
MUST输出格式:
【调查】输入 输出 约束
【主要矛盾】为什么暴力不行
【解法】从矛盾到思路
【代码】
【检验】边界 复杂度

=== 没思路(最高优先级) ===
用户说"没思路/不会/没想法":MUST只输出【调查】+一句话"暴力怎么做?瓶颈在哪?"。MUST NOT提任何算法名称、MUST NOT写代码、MUST NOT给解法方向。
违反后果:用户永远不会自己分析。

=== 诊断代码 ===
MUST顺序:逻辑错→边界漏→工具错→效率低。一次只诊断一层。禁止一次说所有问题。

=== 知识点 ===
MUST先问:"看模板还是理解本质?"根据回答决定输出。

=== 出题 ===
给题目+约束。MUST NOT给答案或提示。结尾:"想清楚主要矛盾,写好了贴给我。"

=== 哲学概念 ===
MUST格式:【原文】【含义】【算法启示】

=== 语录映射 ===
集中优势兵力→二分/双指针
星星之火→动态规划
敌进我退→回溯
群众路线→哈希表
牵一发动全身→链表
没有调查就没有发言权→审题

=== 最后检查 ===
输出前MUST确认:
- 如果用了解法格式,是否四步齐全?
- 如果用户说没思路,是否只做了调查?
- 如果引了语录,是否对应了具体算法?
- 是否有任何装饰性废话?
任一项不通过,修正后再输出。`;

let outputChannel;

function getChannel() {
    if (!outputChannel) {
        outputChannel = vscode.window.createOutputChannel('红宝书');
    }
    return outputChannel;
}

function getConfig() {
    const config = vscode.workspace.getConfiguration('redbook');
    return {
        apiKey: config.get('apiKey', ''),
        apiEndpoint: config.get('apiEndpoint', 'https://api.deepseek.com/chat/completions'),
        model: config.get('model', 'deepseek-chat')
    };
}

function getSelectedOrFileContent() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        return null;
    }
    const selection = editor.selection;
    if (selection && !selection.isEmpty) {
        return editor.document.getText(selection);
    }
    return editor.document.getText();
}

function callDeepSeek(systemPrompt, userMessage) {
    return new Promise((resolve, reject) => {
        const config = getConfig();
        if (!config.apiKey) {
            reject(new Error('API Key 未设置。请运行「红宝书: 设置 API Key」或前往设置填入 redbook.apiKey。'));
            return;
        }

        const body = JSON.stringify({
            model: config.model,
            messages: [
                { role: 'system', content: systemPrompt },
                { role: 'user', content: userMessage }
            ],
            temperature: 0.3,
            max_tokens: 4096
        });

        const url = new URL(config.apiEndpoint);
        const options = {
            hostname: url.hostname,
            port: url.port || (url.protocol === 'https:' ? 443 : 80),
            path: url.pathname + url.search,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${config.apiKey}`,
                'Content-Length': Buffer.byteLength(body)
            }
        };

        const lib = url.protocol === 'https:' ? https : http;
        const req = lib.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => { data += chunk; });
            res.on('end', () => {
                try {
                    const json = JSON.parse(data);
                    if (json.error) {
                        reject(new Error(`API 错误: ${json.error.message || JSON.stringify(json.error)}`));
                        return;
                    }
                    const content = json.choices && json.choices[0] && json.choices[0].message
                        ? json.choices[0].message.content
                        : '';
                    resolve(content);
                } catch (e) {
                    reject(new Error(`解析响应失败: ${e.message}\n原始响应: ${data.substring(0, 500)}`));
                }
            });
        });

        req.on('error', (e) => {
            reject(new Error(`网络请求失败: ${e.message}`));
        });

        req.write(body);
        req.end();
    });
}

function showResult(content, mode) {
    const channel = getChannel();
    channel.clear();
    const titles = {
        analyze: '═══ 红宝书 · 解题分析 ═══',
        guide: '═══ 红宝书 · 引导思考 ═══',
        explain: '═══ 红宝书 · 代码诊断 ═══'
    };
    channel.appendLine(titles[mode] || titles.analyze);
    channel.appendLine('');
    channel.appendLine(content);
    channel.show(true);
}

function showError(message) {
    const channel = getChannel();
    channel.clear();
    channel.appendLine('═══ 红宝书 · 错误 ═══');
    channel.appendLine('');
    channel.appendLine(message);
    channel.show(true);
    vscode.window.showErrorMessage(`红宝书: ${message}`);
}

function activate(context) {
    outputChannel = vscode.window.createOutputChannel('红宝书');
    context.subscriptions.push(outputChannel);

    const analyzeCmd = vscode.commands.registerCommand('redbook.analyze', async () => {
        const content = getSelectedOrFileContent();
        if (!content) {
            vscode.window.showWarningMessage('红宝书: 请先打开文件或选中题目文字。');
            return;
        }

        const channel = getChannel();
        channel.clear();
        channel.appendLine('═══ 红宝书 · 解题分析 ═══');
        channel.appendLine('');
        channel.appendLine('正在调用 DeepSeek 分析...');
        channel.show(true);

        try {
            const userMessage = `请分析这道算法题:\n\n${content}`;
            const result = await callDeepSeek(REDBOOK_SYSTEM_PROMPT, userMessage);
            showResult(result, 'analyze');
        } catch (e) {
            showError(e.message);
        }
    });

    const guideCmd = vscode.commands.registerCommand('redbook.guide', async () => {
        const content = getSelectedOrFileContent();
        if (!content) {
            vscode.window.showWarningMessage('红宝书: 请先打开文件或选中题目文字。');
            return;
        }

        const channel = getChannel();
        channel.clear();
        channel.appendLine('═══ 红宝书 · 引导思考 ═══');
        channel.appendLine('');
        channel.appendLine('正在调用 DeepSeek 分析...');
        channel.show(true);

        try {
            const userMessage = `这道题我没思路，请引导我思考，只做调查不要给答案:\n\n${content}`;
            const result = await callDeepSeek(REDBOOK_SYSTEM_PROMPT, userMessage);
            showResult(result, 'guide');
        } catch (e) {
            showError(e.message);
        }
    });

    const explainCmd = vscode.commands.registerCommand('redbook.explainCode', async () => {
        const content = getSelectedOrFileContent();
        if (!content) {
            vscode.window.showWarningMessage('红宝书: 请先选中要诊断的代码。');
            return;
        }

        const channel = getChannel();
        channel.clear();
        channel.appendLine('═══ 红宝书 · 代码诊断 ═══');
        channel.appendLine('');
        channel.appendLine('正在调用 DeepSeek 逐层诊断...');
        channel.show(true);

        try {
            const userMessage = `请诊断这段代码的错误。按照逻辑错→边界漏→工具错→效率低的顺序，一次只诊断一层:\n\n${content}`;
            const result = await callDeepSeek(REDBOOK_SYSTEM_PROMPT, userMessage);
            showResult(result, 'explain');
        } catch (e) {
            showError(e.message);
        }
    });

    const setApiKeyCmd = vscode.commands.registerCommand('redbook.setApiKey', async () => {
        const key = await vscode.window.showInputBox({
            prompt: '请输入 DeepSeek API Key',
            placeHolder: 'sk-...',
            password: true,
            ignoreFocusOut: true
        });

        if (key !== undefined) {
            const config = vscode.workspace.getConfiguration('redbook');
            await config.update('apiKey', key, vscode.ConfigurationTarget.Global);
            vscode.window.showInformationMessage('红宝书: API Key 已保存到全局设置。');
        }
    });

    context.subscriptions.push(analyzeCmd, guideCmd, explainCmd, setApiKeyCmd);
}

function deactivate() {
    if (outputChannel) {
        outputChannel.dispose();
    }
}

module.exports = { activate, deactivate };
