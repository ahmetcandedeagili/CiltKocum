using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace CiltKocum.Web.Models
{
    public class User
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(100)]
        public string FullName { get; set; }

        [Required]
        [EmailAddress]
        public string Email { get; set; }

        // Skin type classification (e.g., Oily, Dry, Combination, Sensitive)
        [StringLength(50)]
        public string SkinType { get; set; }

        public DateTime CreatedAt { get; set; } = DateTime.Now;

        // Navigation property: A user can have multiple analysis histories
        public ICollection<AnalysisHistories> AnalysisHistories { get; set; }
    }
}