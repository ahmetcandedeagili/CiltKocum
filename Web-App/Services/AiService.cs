using CiltKocum.Web.Models; 
using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace CiltKocum.Web.Services
{
    public class AiService
    {
        private readonly HttpClient _httpClient;

        public AiService(HttpClient httpClient)
        {
            _httpClient = httpClient;

            // Set timeout to 60 seconds (LLM processing might take 10-15 seconds)
            _httpClient.Timeout = TimeSpan.FromSeconds(60);
        }

        // Changed return type from Task<string> to Task<AiResponseDto>
        public async Task<AiResponseDto> AskCiltKocumAiAsync(string userQuestion)
        {
            // The URL of our Python FastAPI microservice
            var apiUrl = "http://127.0.0.1:8000/yapay-zeka/sor";

            // Match the Python 'UserRequest' schema: {"query": "..."}
            var requestBody = new { query = userQuestion };
            var jsonContent = new StringContent(JsonSerializer.Serialize(requestBody), Encoding.UTF8, "application/json");

            try
            {
                // Send the POST request to Python AI
                var response = await _httpClient.PostAsync(apiUrl, jsonContent);

                if (response.IsSuccessStatusCode)
                {
                    var responseData = await response.Content.ReadAsStringAsync();

                    // Automatically convert the JSON string into our C# DTO object
                    var aiResponse = JsonSerializer.Deserialize<AiResponseDto>(responseData);

                    return aiResponse;
                }
                else
                {
                    // Log or handle non-success status codes (e.g., 500 Internal Server Error)
                    return CreateFallbackResponse("CiltKocum AI is currently resting. Please try again later.");
                }
            }
            catch (Exception ex)
            {
                // Catch any connection errors (like Python server being closed)
                return CreateFallbackResponse($"Connection error: {ex.Message}");
            }
        }

        // Helper method to generate a safe fallback DTO if things go wrong
        private AiResponseDto CreateFallbackResponse(string errorMessage)
        {
            return new AiResponseDto
            {
                ResponseText = errorMessage,
                ActiveIngredient = "Error",
                LiveProducts = new System.Collections.Generic.List<LiveProductDto>()
            };
        }
    }
}