document.addEventListener("DOMContentLoaded", function () {
  var input = document.getElementById("api-key");
  var saveBtn = document.getElementById("save");
  var status = document.getElementById("status");

  chrome.storage.local.get(["redbook_api_key"], function (result) {
    if (result.redbook_api_key) {
      input.value = result.redbook_api_key;
      status.textContent = "✅ API Key 已设置";
      status.className = "success";
    }
  });

  saveBtn.addEventListener("click", function () {
    var key = input.value.trim();
    if (!key) {
      status.textContent = "❌ 请输入 API Key";
      status.className = "error";
      return;
    }
    chrome.storage.local.set({ redbook_api_key: key }, function () {
      status.textContent = "✅ 保存成功";
      status.className = "success";
    });
  });
});
