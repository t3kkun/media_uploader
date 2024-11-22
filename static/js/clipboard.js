function copyToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
        // Clipboard APIがサポートされている場合
        navigator.clipboard.writeText(text).then(() => {
            alert("Copied to clipboard!");
        }).catch(err => {
            console.error("Failed to copy text: ", err);
        });
    } else {
        // Clipboard APIがサポートされていない場合
        fallbackCopyToClipboard(text);
    }
}

function fallbackCopyToClipboard(text) {
    // テキストエリアを動的に作成
    const textArea = document.createElement("textarea");
    textArea.value = text;
    document.body.appendChild(textArea);

    // テキストを選択してコピー
    textArea.select();
    textArea.setSelectionRange(0, textArea.value.length); // モバイル端末用
    try {
        document.execCommand("copy");
        alert("Copied to clipboard!");
    } catch (err) {
        console.error("Fallback: Failed to copy text: ", err);
    }

    // テキストエリアを削除
    document.body.removeChild(textArea);
}
