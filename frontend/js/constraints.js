const fapi = "http://127.0.0.1:8000";

const paths = {
    CHAT: "/chat",
    ID:"/id",
    JSON:"/json",
    CHAT_HISTORY: "/chat_history",
    CHAT_LOGS: "/chat_logs",
    RATINGS: "/ratings",
    OVERALL_RATING: "/ratings/overall",
    STUDENTS: "/students",
    STUDENT: "/students/<id>",
    TEACHERS: "/teachers",
    TEACHER: "/teacher/<name>",
    PERIODS: "/periods",
    PERIOD: "/periods/<number>",
    GET_ASSIGNMENTS_ON_GOOGLE_CLASSROOM: "/classroom",
};

// Automagically prepend the base URL to every path
export const APIs = Object.fromEntries(
    Object.entries(paths).map(([key, path]) => [key, `${fapi}${path}`])
);

APIs.PEPPER_JSON = "Pepper.json";