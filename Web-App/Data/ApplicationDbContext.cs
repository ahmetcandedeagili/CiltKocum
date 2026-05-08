using CiltKocum.Web.Models;
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;

namespace CiltKocum.Web.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options)
        {
        }

        // MS SQL Server'da oluşacak İngilizce tablolarımız
        public DbSet<User> Users { get; set; }
        public DbSet<Product> Products { get; set; }
        public DbSet<AnalysisHistories> AnalysisHistories { get; set; }
    }
}