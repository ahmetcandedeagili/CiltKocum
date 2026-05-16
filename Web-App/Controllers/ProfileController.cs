using CiltKocum.Web.Data;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;

namespace CiltKocum.Web.Controllers
{
    [Authorize] // Restrict access to authenticated sessions only
    public class ProfileController : Controller
    {
        private readonly ApplicationDbContext _context;

        public ProfileController(ApplicationDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<IActionResult> Index()
        {
            // Pull unique Identifier key belonging to current user context
            var userIdString = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
            if (int.TryParse(userIdString, out int userId))
            {
                // Pull historical timeline analytics items linked to target profile identity
                var historyRecords = await _context.AnalysisHistories
                    .Where(h => h.UserId == userId)
                    .OrderByDescending(h => h.AnalysisDate)
                    .ToListAsync();

                return View(historyRecords);
            }

            return RedirectToAction("Login", "Auth");
        }
    }
}