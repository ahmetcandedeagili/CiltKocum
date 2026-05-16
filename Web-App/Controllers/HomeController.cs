using CiltKocum.Web.Data;
using CiltKocum.Web.Models;
using CiltKocum.Web.Services;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Threading.Tasks;
using System.Security.Claims; // Kullanýcý ID'sini çekmek için gerekli

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

        [HttpPost]
        public async Task<IActionResult> AskRoutine(string question)
        {
            if (string.IsNullOrWhiteSpace(question))
            {
                ViewBag.Error = "Please describe your skin problem in detail.";
                return View("Index");
            }

            // 1. Get the DTO package from Python API (Contains Text, Ingredient, and Products)
            var aiResponseDto = await _aiService.AskCiltKocumAiAsync(question);

            // 2. EÐER KULLANICI GÝRÝÞ YAPMIÞSA VERÝTABANINA KAYDET (YENÝ EKLENEN KISIM)
            if (User.Identity.IsAuthenticated)
            {
                var userIdString = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
                if (int.TryParse(userIdString, out int userId))
                {
                    var analysisLog = new AnalysisHistories
                    {
                        UserId = userId,
                        UserQuestion = question,
                        AiResponse = aiResponseDto.ResponseText,
                        RecommendedIngredient = aiResponseDto.ActiveIngredient,
                        AnalysisDate = DateTime.Now
                    };

                    _context.AnalysisHistories.Add(analysisLog);
                    await _context.SaveChangesAsync();
                }
            }

            // 3. Pass the extracted data to the View using ViewBag
            ViewBag.UserQuestion = question;
            ViewBag.AiAnswer = aiResponseDto.ResponseText;
            ViewBag.ActiveIngredient = aiResponseDto.ActiveIngredient;
            ViewBag.RecommendedProducts = aiResponseDto.LiveProducts;

            return View("Index");
        }
    }
}