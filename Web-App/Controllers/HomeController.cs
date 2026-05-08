using CiltKocum.Web.Data;
using CiltKocum.Web.Models;
using CiltKocum.Web.Services;
using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;

namespace CiltKocum.Web.Controllers
{
    public class HomeController : Controller
    {
        private readonly AiService _aiService;
        private readonly ApplicationDbContext _context;

        // Injecting AI Service and Database Context
        public HomeController(AiService aiService, ApplicationDbContext context)
        {
            _aiService = aiService;
            _context = context;
        }

        public IActionResult Index()
        {
            return View();
        }

        [HttpPost] // Removed the duplicate [HttpPost]
        public async Task<IActionResult> AskRoutine(string question)
        {
            if (string.IsNullOrWhiteSpace(question))
            {
                ViewBag.Error = "Please describe your skin problem in detail.";
                return View("Index");
            }

            // 1. Get the DTO package from Python API (Contains Text, Ingredient, and Products)
            var aiResponseDto = await _aiService.AskCiltKocumAiAsync(question);

            // 2. Pass the extracted data to the View using ViewBag
            ViewBag.UserQuestion = question;

            // We specify .ResponseText because aiResponseDto is an object, not a string
            ViewBag.AiAnswer = aiResponseDto.ResponseText;

            ViewBag.ActiveIngredient = aiResponseDto.ActiveIngredient;

            // We don't need C# DB matching anymore! Python already found the products for us.
            ViewBag.RecommendedProducts = aiResponseDto.LiveProducts;

            // TODO for later: Save this interaction to AnalysisHistories table

            return View("Index");
        }
    }
}