public static class PointsManager
{
    private static int userID;
    private static int points;

    public static int GetPoints(int userid)
    {
        //TO IMPLEMENT
        //Get points from database
        points = userid;
        userID = userid;
        return points;
    }
    public static string GetLeaderboard(int userid)
    {
        //TO IMPLEMENT
        //Get Leaderboard from database
        string s = "Leaderboard from database";
        return s;
    }

}
