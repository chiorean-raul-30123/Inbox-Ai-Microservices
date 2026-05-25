import { Navigate } from "react-router-dom";
import type { ReactNode } from "react";

import { useAuth } from "./AuthContext";

export function ProtectedRoute({children}: { children: ReactNode}){
    const {isAuthenticated, isLoading} = useAuth();
    
    if(isLoading){
        return <div className="p-8 text-slate-600">Loading...</div>
    }

    if(!isAuthenticated){
        return <Navigate to="/login" replace />;
    }

    return children;

}