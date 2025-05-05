import { createContext, ReactNode, useContext, useEffect, useState } from "react";

interface AuthContextType {
    isLoggedIn: boolean;
    login: (token: string) => void;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({children} : {children: ReactNode}) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        setIsLoggedIn(!!token);
    }, []);

    const login = (token: string) => {
        localStorage.setItem('access_token', token);
        setIsLoggedIn(true);
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        setIsLoggedIn(false);
    };

    return (
        <AuthContext.Provider value={{isLoggedIn, login, logout}}>
            {children}
        </AuthContext.Provider>
    )
};

export const useAuth = () : AuthContextType => {
    const context = useContext(AuthContext);
    if (context == undefined) throw new Error('useAuth must be used within an AuthProvider');
    return context;
}