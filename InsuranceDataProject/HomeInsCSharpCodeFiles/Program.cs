using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Data.SqlClient;

namespace _2ndCSharpSQLProject
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.Write("Please enter the PropertyID: ");
            var propID = int.Parse(Console.ReadLine());
            RetrievePropDetails(propID);
        }

        private static string InsConnection()
        {
            var connectionString = @"C:\Users\richm\source\repos\HomeInsCSharpCodeFiles\insConnectionString.TXT";
            using (FileStream fs = File.OpenRead(connectionString))
            {
                using (StreamReader str = new StreamReader(fs))
                {
                    return str.ReadLine();
                }
            }
        }
        private static void RetrievePropDetails(int propID)
        {
            SqlConnection insConnect = new SqlConnection(InsConnection());
            SqlCommand propCommand = new SqlCommand("SELECT * FROM Property WHERE PropID =" + propID, insConnect);

            propCommand.Connection.Open();

            SqlDataReader tableReader;

            try
            {
                tableReader = propCommand.ExecuteReader();

                if (tableReader.Read())
                {
                    var result = new Object[tableReader.FieldCount];
                    Console.WriteLine(result);
                    int numFields = tableReader.GetValues(result);
                    Console.WriteLine(numFields);

                    Console.WriteLine("The data for this property is as follows: ");
                    foreach (var item in result)
                    {
                        Console.Write(item + "|");
                    }
                }
                
            }
            catch
            {
                Console.WriteLine("There was a problem attempting the SELECT statement.");
            }

            propCommand.Connection.Close();
        }
    }
}
