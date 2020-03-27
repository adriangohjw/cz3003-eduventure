public static class CropManager
{
    private static string[] crops;

    static CropManager()
    {
        crops = new string[6]{"Sunflower","Grapes","Pumpkins","Blueberries","Cabbage","Strawberries"};
    }
    public static string[] GetCropsNames(int userid)
    {
        //TO IMPLEMENT
        //Get Crops Levels from Database
        return crops;
    }
    public static string[] GetCropsMenu(string name)
    {
        //TO IMPLEMENT
        //Get Crop Menu Statistics from Database
        string[] cropContent = new string[2]{name.ToString(),name.ToString()+" Statistics from database.."};
        return cropContent;
    }
}
