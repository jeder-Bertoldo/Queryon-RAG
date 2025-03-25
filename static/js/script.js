/* 
// Se não usa mais o upload-form, comente ou remova este trecho
// document.getElementById("upload-form").onsubmit = async (e) => {
//     e.preventDefault();
//     const formData = new FormData(e.target);
//     const response = await fetch('/upload', {
//         method: 'POST',
//         body: formData
//     });
//     const result = await response.json();
//     alert(result.message || result.error);
// };
*/

/**
 * Função que exibe texto em um elemento de forma progressiva (efeito de digitação).
 * @param {HTMLElement} element - O elemento onde o texto será exibido.
 * @param {string} text - O texto completo a ser exibido.
 * @param {number} speed - Intervalo (ms) entre cada caractere.
 * @param {function} callback - Função opcional a ser chamada ao final da "digitação".
 */
function typeWriterEffect(element, text, speed = 10, callback) {
  let i = 0;
  element.textContent = "";
  
  function typing() {
    if (i < text.length) {
      element.textContent += text.charAt(i);
      i++;
      setTimeout(typing, speed);
    } else {
      if (callback) callback();
    }
  }
  
  typing();
}

async function sendQuery() {
  const queryInput = document.getElementById("query");
  const messagesContainer = document.getElementById("messages");
  const responseElement = document.getElementById("response"); // Se existir no HTML

  // 1) Captura o texto digitado e valida
  const query = queryInput.value.trim();
  if (!query) return;

  // 2) Exibe a mensagem do usuário em um balão
  const userMessage = document.createElement("div");
  userMessage.classList.add("user-message");
  userMessage.innerText = query;
  messagesContainer.appendChild(userMessage);

  // 3) Limpa o campo de texto
  queryInput.value = "";

  // 4) Cria um balão vazio para a resposta do assistente (efeito de digitação)
  const assistantMessage = document.createElement("div");
  assistantMessage.classList.add("assistant-message");
  messagesContainer.appendChild(assistantMessage);

  try {
    // 5) Faz a requisição ao servidor
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query })
    });
    const result = await response.json();

    // 6) Efeito de digitação no balão do assistente
    typeWriterEffect(
      assistantMessage, 
      result.response, 
      30, 
      () => {
        if (responseElement) {
          responseElement.textContent = result.response;
        }
      }
    );

  } catch (error) {
    assistantMessage.innerText = "Ocorreu um erro ao obter a resposta.";
    if (responseElement) {
      responseElement.textContent = "Ocorreu um erro ao obter a resposta.";
    }
    console.error(error);
  }
}

// Adiciona o listener de Enter ao input #query
document.addEventListener("DOMContentLoaded", () => {
  const queryInput = document.getElementById("query");
  if (queryInput) {
    // Se o usuário pressionar Enter (sem Shift), envia a mensagem
    queryInput.addEventListener("keydown", function (event) {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendQuery();
      }
    });
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const themeToggle = document.getElementById("theme-toggle");
  const sunIcon = themeToggle.querySelector(".icon-sun");
  const moonIcon = themeToggle.querySelector(".icon-moon");

  themeToggle.addEventListener("click", function () {
    // Alterna o tema
    document.body.classList.toggle("light-mode");

    // Gera a rotação
    themeToggle.style.transform = "rotate(360deg)";
    setTimeout(() => {
      themeToggle.style.transform = "";
    }, 500);

    // Alterna os ícones
    if (document.body.classList.contains("light-mode")) {
      sunIcon.style.display = "none";
      moonIcon.style.display = "inline-block";
    } else {
      sunIcon.style.display = "inline-block";
      moonIcon.style.display = "none";
    }
  });
});
