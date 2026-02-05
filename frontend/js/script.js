document.addEventListener('DOMContentLoaded', () => {
    const originalTextarea = document.getElementById('originalText');
    const convertedTextarea = document.getElementById('convertedText');
    const charCountSpan = document.getElementById('currentCharCount');
    const targetAudienceRadios = document.querySelectorAll('input[name="targetAudience"]');
    const convertButton = document.getElementById('convertButton');
    const copyButton = document.getElementById('copyButton');
    const errorMessageDiv = document.getElementById('errorMessage');
    const copyFeedbackDiv = document.getElementById('copyFeedback');

    const MAX_CHARS = 500;
    const API_ENDPOINT = '/api/convert'; // Assuming backend is on the same host/port

    // Function to update character count
    const updateCharCount = () => {
        const currentLength = originalTextarea.value.length;
        charCountSpan.textContent = currentLength;
        if (currentLength > MAX_CHARS) {
            originalTextarea.value = originalTextarea.value.substring(0, MAX_CHARS);
            charCountSpan.textContent = MAX_CHARS;
        }
    };

    // Initial character count update
    updateCharCount();

    // Event listener for input textarea
    originalTextarea.addEventListener('input', updateCharCount);

    // Function to display error message
    const displayErrorMessage = (message) => {
        errorMessageDiv.textContent = message;
        errorMessageDiv.style.display = 'block';
    };

    // Function to hide error message
    const hideErrorMessage = () => {
        errorMessageDiv.textContent = '';
        errorMessageDiv.style.display = 'none';
    };

    // Function to display copy feedback
    const displayCopyFeedback = (message, isSuccess = true) => {
        copyFeedbackDiv.textContent = message;
        copyFeedbackDiv.style.color = isSuccess ? 'var(--success-color)' : 'var(--error-color)';
        copyFeedbackDiv.style.display = 'block';
        setTimeout(() => {
            copyFeedbackDiv.textContent = '';
            copyFeedbackDiv.style.display = 'none';
        }, 2000);
    };

    // Event listener for convert button
    convertButton.addEventListener('click', async () => {
        const originalText = originalTextarea.value.trim();
        const selectedTarget = document.querySelector('input[name="targetAudience"]:checked').value;

        hideErrorMessage();
        convertedTextarea.value = ''; // Clear previous result
        convertButton.disabled = true;
        convertButton.textContent = '변환 중...'; // Indicate loading

        if (!originalText) {
            displayErrorMessage('변환할 내용을 입력해주세요.');
            convertButton.disabled = false;
            convertButton.textContent = '변환하기';
            return;
        }

        try {
            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: originalText, target: selectedTarget }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            convertedTextarea.value = data.converted_text;

        } catch (error) {
            console.error('Conversion error:', error);
            displayErrorMessage(`오류가 발생했습니다: ${error.message}. 잠시 후 다시 시도해주세요.`);
        } finally {
            convertButton.disabled = false;
            convertButton.textContent = '변환하기';
        }
    });

    // Event listener for copy button
    copyButton.addEventListener('click', async () => {
        if (convertedTextarea.value) {
            try {
                await navigator.clipboard.writeText(convertedTextarea.value);
                displayCopyFeedback('클립보드에 복사되었습니다!');
            } catch (err) {
                console.error('Failed to copy text:', err);
                displayCopyFeedback('복사 실패!', false);
            }
        } else {
            displayCopyFeedback('변환 결과가 없습니다.', false);
        }
    });
});