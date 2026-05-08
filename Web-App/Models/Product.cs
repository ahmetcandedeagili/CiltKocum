using System.ComponentModel.DataAnnotations;

namespace CiltKocum.Web.Models
{
    public class Product
    {
        [Key]
        public int Id { get; set; }

        // The brand of the product (Nullable since API might send brand and name together)
        public string? Brand { get; set; }

        [Required]
        public string Name { get; set; }

        // The specific active ingredient required for the product (e.g., Salicylic Acid)
        [Required]
        public string ActiveIngredient { get; set; }

        // Price data retrieved from the Python API
        public string? Price { get; set; }

        // URL for the product image to render in HTML
        public string? ImageUrl { get; set; }

        // External link to purchase the product
        public string? PurchaseLink { get; set; }

        // Fields for future use (currently not provided by the API)
        public string? SuitableSkinTypes { get; set; }
        public string? Purpose { get; set; }
    }
}