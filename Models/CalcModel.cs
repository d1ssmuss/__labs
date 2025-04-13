using System.ComponentModel.DataAnnotations;

namespace TryTwo.Models
{
    public class CalcModel
    {
        [StringLength(10, MinimumLength = 2, ErrorMessage = " Длинна числа должна быть от 2 до 10")]
        public string firstNum { get; set; }
        [Required(ErrorMessage = "Пожалуйста, Введите число.")]
       
        public uint? secondNum { get; set; }

        public double result { get; set; }

        
        public List<string> operation { get; set; }

        public uint compareNum { get; set; }

        
        public CalcModel()
        {
            operation = new List<string>();
        }



    }
}
