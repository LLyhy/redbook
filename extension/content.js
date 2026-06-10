(function () {
  "use strict";

  const REDBOOK_SYSTEM_PROMPT = `你是红宝书，以毛主席《矛盾论》《实践论》为方法论分析算法问题。核心人格：任何算法问题本质是矛盾（已知vs所求），先找主要矛盾再选解法，语录必须对应具体算法，简洁务实不搞形式主义。解题格式：【调查】输入/输出/约束→【主要矛盾】一句话→【解法】逻辑推导→【代码】→【检验】边界/复杂度。用户说没思路：只做调查不给答案，禁止提任何算法名称。诊断代码：逻辑→边界→工具→效率，一次只诊断一层。语录映射：集中优势兵力→二分/双指针，星星之火→DP，敌进我退→回溯，群众路线→哈希表。`;

  let sidebar = null;
  let floatingBtn = null;
  let currentMode = "analyze";

  function getProblemTitle() {
    const selectors = [
      '[data-cy="question-title"]',
      ".text-title-large",
      ".css-10o4wqw",
      '[class*="question-title"]',
      "h4 a",
      ".question-title",
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el) return el.textContent.trim();
    }
    return document.title.split(" - ")[0].trim() || "未知题目";
  }

  function getProblemDescription() {
    const selectors = [
      '[data-track-load="description_content"]',
      ".xFUwe",
      ".description__24sA",
      '[class*="question-content"]',
      ".question-description",
      '[class*="description"]',
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el && el.textContent.trim().length > 20) {
        return el.textContent.trim().substring(0, 3000);
      }
    }
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) return metaDesc.content.trim();
    return "";
  }

  function getApiKey() {
    return new Promise(function (resolve) {
      chrome.storage.local.get(["redbook_api_key"], function (result) {
        resolve(result.redbook_api_key || "");
      });
    });
  }

  async function callDeepSeek(userMessage, mode) {
    const apiKey = await getApiKey();
    if (!apiKey) {
      throw new Error("请先设置 API Key");
    }

    let fullUserMessage;
    if (mode === "guide") {
      fullUserMessage =
        "我没思路，请只做调查，不要给答案，不要提任何算法名称，不要写代码。\n\n" +
        userMessage;
    } else {
      fullUserMessage = "请分析这道题：\n\n" + userMessage;
    }

    const response = await fetch("https://api.deepseek.com/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + apiKey,
      },
      body: JSON.stringify({
        model: "deepseek-chat",
        messages: [
          { role: "system", content: REDBOOK_SYSTEM_PROMPT },
          { role: "user", content: fullUserMessage },
        ],
        temperature: 0.6,
        max_tokens: 4096,
      }),
    });

    if (!response.ok) {
      const err = await response.json().catch(function () {
        return {};
      });
      throw new Error(
        err.error?.message || "API 请求失败 (HTTP " + response.status + ")"
      );
    }

    const data = await response.json();
    return data.choices[0].message.content;
  }

  function createSidebar() {
    sidebar = document.createElement("div");
    sidebar.id = "redbook-sidebar";
    sidebar.innerHTML =
      '<div id="redbook-sidebar-header">' +
      "<h2>📕 红宝书</h2>" +
      '<button id="redbook-sidebar-close">✕</button>' +
      "</div>" +
      '<div id="redbook-sidebar-body">' +
      "</div>";
    document.body.appendChild(sidebar);

    document
      .getElementById("redbook-sidebar-close")
      .addEventListener("click", function () {
        sidebar.classList.remove("open");
        if (floatingBtn) floatingBtn.classList.remove("hidden");
      });
  }

  function createFloatingButton() {
    floatingBtn = document.createElement("button");
    floatingBtn.id = "redbook-floating-btn";
    floatingBtn.textContent = "红宝书";
    floatingBtn.title = "红宝书 · LeetCode 助手";
    document.body.appendChild(floatingBtn);

    floatingBtn.addEventListener("click", function () {
      if (!sidebar) createSidebar();
      renderSidebarBody();
      sidebar.classList.add("open");
      floatingBtn.classList.add("hidden");
    });
  }

  function renderSidebarBody() {
    if (!sidebar) return;
    var body = sidebar.querySelector("#redbook-sidebar-body");
    var title = getProblemTitle();
    var desc = getProblemDescription();

    body.innerHTML = "";

    var problemInfo = document.createElement("div");
    problemInfo.className = "problem-info";
    problemInfo.innerHTML =
      "<h3>" +
      escapeHtml(title) +
      "</h3>" +
      "<p>" +
      escapeHtml(desc.substring(0, 200)) +
      (desc.length > 200 ? "..." : "") +
      "</p>";
    body.appendChild(problemInfo);

    var modeSelector = document.createElement("div");
    modeSelector.className = "mode-selector";

    var analyzeBtn = document.createElement("button");
    analyzeBtn.className =
      "mode-analyze" + (currentMode === "analyze" ? " active" : "");
    analyzeBtn.textContent = "🔍 分析";
    analyzeBtn.addEventListener("click", function () {
      currentMode = "analyze";
      renderSidebarBody();
    });

    var guideBtn = document.createElement("button");
    guideBtn.className =
      "mode-guide" + (currentMode === "guide" ? " active" : "");
    guideBtn.textContent = "💡 引导";
    guideBtn.addEventListener("click", function () {
      currentMode = "guide";
      renderSidebarBody();
    });

    modeSelector.appendChild(analyzeBtn);
    modeSelector.appendChild(guideBtn);
    body.appendChild(modeSelector);

    var apiCheckContainer = document.createElement("div");
    apiCheckContainer.id = "redbook-api-check";
    body.appendChild(apiCheckContainer);

    var actionContainer = document.createElement("div");
    actionContainer.id = "redbook-action";
    body.appendChild(actionContainer);

    var resultContainer = document.createElement("div");
    resultContainer.id = "redbook-result";
    body.appendChild(resultContainer);

    loadApiKeySection(apiCheckContainer, actionContainer, resultContainer, title, desc);
  }

  function loadApiKeySection(apiCheckContainer, actionContainer, resultContainer, title, desc) {
    getApiKey().then(function (apiKey) {
      if (!apiKey) {
        renderApiKeyInput(apiCheckContainer);
        actionContainer.innerHTML = "";
        resultContainer.innerHTML = "";
      } else {
        apiCheckContainer.innerHTML = "";
        renderAskButton(actionContainer, resultContainer, title, desc);
      }
    });
  }

  function renderApiKeyInput(container) {
    container.innerHTML =
      '<div class="no-api-key">' +
      "<p>⚙️ 请设置 DeepSeek API Key</p>" +
      '<input type="password" id="redbook-api-key-input" placeholder="sk-..." />' +
      '<button id="redbook-save-key">保存</button>' +
      "</div>";

    document.getElementById("redbook-save-key").addEventListener("click", function () {
      var key = document.getElementById("redbook-api-key-input").value.trim();
      if (!key) return;
      chrome.storage.local.set({ redbook_api_key: key }, function () {
        renderSidebarBody();
      });
    });
  }

  function renderAskButton(actionContainer, resultContainer, title, desc) {
    var askBtn = document.createElement("button");
    askBtn.className = "ask-btn";
    askBtn.textContent =
      currentMode === "analyze" ? "🔍 开始分析" : "💡 给我引导";
    askBtn.addEventListener("click", function () {
      handleAsk(resultContainer, title, desc);
    });
    actionContainer.innerHTML = "";
    actionContainer.appendChild(askBtn);

    if (!resultContainer.querySelector(".result") && !resultContainer.querySelector(".loading")) {
      resultContainer.innerHTML =
        '<div class="empty-state">' +
        '<span class="icon">📕</span>' +
        "<p>点击上方按钮</p>" +
        "<p>" +
        (currentMode === "analyze" ? "用矛盾分析法分析此题" : "只做调查，不给答案") +
        "</p>" +
        "</div>";
    }
  }

  async function handleAsk(resultContainer, title, desc) {
    resultContainer.innerHTML =
      '<div class="loading">' +
      '<div class="spinner"></div>' +
      "<span>思考中...</span>" +
      "</div>";

    var disableBtn = document.querySelector("#redbook-action .ask-btn");
    if (disableBtn) disableBtn.disabled = true;

    try {
      var userMessage =
        "题目：" +
        title +
        "\n\n题目描述：\n" +
        (desc || "(未能自动获取，请查看页面)");
      var result = await callDeepSeek(userMessage, currentMode);
      resultContainer.innerHTML =
        '<div class="result">' + formatResult(result) + "</div>";
    } catch (err) {
      resultContainer.innerHTML =
        '<div class="error">❌ ' + escapeHtml(err.message) + "</div>";
    } finally {
      if (disableBtn) disableBtn.disabled = false;
    }
  }

  function formatResult(text) {
    return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/```(\w*)\n([\s\S]*?)```/g, function (match, lang, code) {
        return "<pre><code>" + code.replace(/\n$/, "") + "</code></pre>";
      })
      .replace(
        /【(\w+)】/g,
        '<strong style="color:#c41e1e;">【$1】</strong>'
      )
      .replace(/\n/g, "<br>");
  }

  function escapeHtml(str) {
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function init() {
    if (document.getElementById("redbook-floating-btn")) return;

    var path = window.location.pathname;
    if (
      !path.includes("/problems/") ||
      path.endsWith("/problems/") ||
      path.endsWith("/problems")
    ) {
      return;
    }

    createFloatingButton();
    createSidebar();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
