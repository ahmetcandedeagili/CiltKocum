using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace CiltKocum.Web.Models
{
    public class AnalysisHistories
    {
        [Key]
        public int Id { get; set; }

        // Foreign key relationship with the User table
        public int UserId { get; set; }

        [ForeignKey("UserId")]
        public User User { get; set; }

        [Required]
        public string UserQuestion { get; set; }

        [Required]
        public string AiResponse { get; set; }

        // The specific active ingredient recommended by the AI during this session
        public string? RecommendedIngredient { get; set; }

        public DateTime AnalysisDate { get; set; } = DateTime.Now;
    }
}