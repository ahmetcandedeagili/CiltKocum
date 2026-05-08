using CiltKocum.Web.Data;
using CiltKocum.Web.Services;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container (MVC architecture)
builder.Services.AddControllersWithViews();

// 1. Setup Database connection to SQL Server
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// 2. Register our AI Service with HttpClient to talk with Python
builder.Services.AddHttpClient<AiService>();

var app = builder.Build();

// Configure the HTTP request pipeline for production/development
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    // Secure headers
    app.UseHsts();
}

// --- DATABASE AUTO-SEEDER (Runs only if DB is empty) ---
// Note: Python API handles live product matching now, but we keep some local data for backup
using (var scope = app.Services.CreateScope())
{
    var services = scope.ServiceProvider;
    var context = services.GetRequiredService<ApplicationDbContext>();

    // If there are no products in the DB, inject these dummy products
    if (!context.Products.Any())
    {
        context.Products.AddRange(
            new CiltKocum.Web.Models.Product
            {
                Brand = "Cosrx",
                Name = "BHA Blackhead Power Liquid",
                ActiveIngredient = "Salicylic Acid",
                Price = "$22.00",
                PurchaseLink = "https://www.sephora.com",
                SuitableSkinTypes = "Oily, Combination",
                Purpose = "Blackhead and Acne Control",
                ImageUrl = "https://cdn.dsmcdn.com/ty41/product/media/images/20210106/15/45686380/64467383/1/1_org_zoom.jpg"
            },
            new CiltKocum.Web.Models.Product
            {
                Brand = "The Ordinary",
                Name = "Niacinamide 10% + Zinc 1%",
                ActiveIngredient = "Niacinamide",
                Price = "$10.00",
                PurchaseLink = "https://www.sephora.com",
                SuitableSkinTypes = "All Skin Types",
                Purpose = "Sebum Control",
                ImageUrl = "https://cdn.dsmcdn.com/ty148/product/media/images/20210717/14/111059952/56961448/1/1_org_zoom.jpg"
            }
        );
        context.SaveChanges(); // Save changes to MS SQL
    }
}
// --- AUTO-SEEDER END ---

app.UseHttpsRedirection();
app.UseRouting();

app.UseAuthorization();

app.MapStaticAssets();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}")
    .WithStaticAssets();

app.Run();