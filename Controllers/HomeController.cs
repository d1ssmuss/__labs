using System.Diagnostics;
using System.Reflection;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.Extensions.Options;
using Newtonsoft.Json.Linq;
using TryTwo.Models;


namespace TryTwo.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;

        public IActionResult PrintRes()
        {
            return View(); 
        }
        public HomeController(ILogger<HomeController> logger)
        {
            _logger = logger;
        }

        public ViewResult Index(CalcModel model,string action )
        {
            if (action == "reset")
            {

                
                model.operation = ["0"];
                ViewBag.result = null;
                ViewBag.compare = 0;
                ModelState.Clear();
                return View();
            }
            else
            {

                var selectedValues = model.operation;
                if (ModelState.IsValid)
                {
                    if (selectedValues != null && selectedValues.Count > 0)
                    {

                        char charOperation = Convert.ToChar(selectedValues[0]);

                        switch (charOperation)
                        {
                            case '+':
                                model.result = Convert.ToDouble(model.firstNum) + Convert.ToDouble(model.secondNum);
                                ViewBag.result = model.result;
                                ViewBag.compare = model.compareNum;
                                ViewBag.FrNum = model.firstNum;
                                ViewBag.SecNum = model.secondNum;
                                ViewBag.oper = charOperation;
                                return View();

                            case '-':

                                model.result = Convert.ToDouble(model.firstNum) - Convert.ToDouble(model.secondNum);
                                ViewBag.result = model.result;
                                ViewBag.compare = model.compareNum;
                                ViewBag.FrNum = model.firstNum;
                                ViewBag.SecNum = model.secondNum;
                                ViewBag.oper = charOperation;
                                return View();
                            case '*':
                                model.result = Convert.ToDouble(model.firstNum) * Convert.ToDouble(model.secondNum);
                                ViewBag.result = model.result;
                                ViewBag.compare = model.compareNum;
                                ViewBag.FrNum = model.firstNum;
                                ViewBag.SecNum = model.secondNum;
                                ViewBag.oper = charOperation;
                                return View();
                            case '/':
                                switch (Convert.ToDouble(model.secondNum))
                                {

                                    case 0:
                                        ModelState.AddModelError("", "Ошибка: деление на ноль.");

                                        return View();
                                    default:
                                        model.result = Convert.ToDouble(model.firstNum) / Convert.ToDouble(model.secondNum);
                                        ViewBag.result = model.result;
                                        ViewBag.compare = model.compareNum;
                                        ViewBag.FrNum = model.firstNum;
                                        ViewBag.SecNum = model.secondNum;
                                        ViewBag.oper = charOperation;

                                        return View();
                                }


                        }

                    }
                }
                
                return View();
            }
        }

        public ViewResult Dubler(CalcModel model, string action)
        {
            string equals = "=";
            var FrNum = Request.Query["FrNum"];
            ViewBag.FrNum = FrNum;
            var SecNum = Request.Query["SecNum"];
            ViewBag.SecNum = SecNum;
            string oper = Request.Query["oper"];
            ViewBag.oper = oper.Replace("+", "плюс").Replace("-", "минус").Replace("*", "умножить").Replace("/", "деление").PadRight(8);
            var res = Request.Query["res"];
            ViewBag.res = res;
            ViewBag.equals = equals.Replace("=", "равно").PadRight(2); 
            return View();
        }

        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
