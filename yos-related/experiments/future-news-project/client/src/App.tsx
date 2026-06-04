import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Route, Switch } from "wouter";
import ErrorBoundary from "./components/ErrorBoundary";
import { ThemeProvider } from "./contexts/ThemeContext";
import { LanguageProvider } from "./contexts/LanguageContext";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import Article from "./pages/Article";
import RoutePage from "./pages/Route";
import Edition from "./pages/Edition";
import Confluence from "./pages/Confluence";
import MapPage from "./pages/MapPage";
import Futura from "./pages/Futura";
import Method from "./pages/Method";
import NotFound from "./pages/NotFound";

function Router() {
  return (
    <Layout>
      <Switch>
        <Route path="/" component={Home} />
        <Route path="/article/:id" component={Article} />
        <Route path="/route/:id" component={RoutePage} />
        <Route path="/edition" component={Edition} />
        <Route path="/confluence/:id" component={Confluence} />
        <Route path="/map" component={MapPage} />
        <Route path="/futura" component={Futura} />
        <Route path="/method" component={Method} />
        <Route path="/404" component={NotFound} />
        <Route component={NotFound} />
      </Switch>
    </Layout>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider defaultTheme="light">
        <LanguageProvider>
          <TooltipProvider>
            <Toaster />
            <Router />
          </TooltipProvider>
        </LanguageProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
