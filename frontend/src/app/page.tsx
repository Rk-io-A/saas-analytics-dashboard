"use client";

import { useState, useEffect } from "react";
import {
  DollarSign,
  Users,
  TrendingDown,
  Activity,
  BarChart3,
  ArrowUpRight,
  ArrowDownRight,
} from "lucide-react";

interface Analytics {
  mrr: number;
  total_revenue: number;
  active_subscribers: number;
  churned_this_month: number;
  churn_rate: number;
  total_subscriptions: number;
}

export default function Dashboard() {
  const [analytics, setAnalytics] = useState<Analytics>({
    mrr: 24850,
    total_revenue: 186400,
    active_subscribers: 142,
    churned_this_month: 8,
    churn_rate: 5.3,
    total_subscriptions: 168,
  });

  // Demo data is shown by default (backend optional)

  const cards = [
    {
      title: "Monthly Recurring Revenue",
      value: `$${analytics.mrr.toLocaleString()}`,
      change: "+12.5%",
      positive: true,
      icon: DollarSign,
      color: "from-emerald-500 to-teal-500",
    },
    {
      title: "Active Subscribers",
      value: analytics.active_subscribers.toString(),
      change: "+8.2%",
      positive: true,
      icon: Users,
      color: "from-blue-500 to-indigo-500",
    },
    {
      title: "Churn Rate",
      value: `${analytics.churn_rate}%`,
      change: "-1.4%",
      positive: true,
      icon: TrendingDown,
      color: "from-orange-500 to-red-500",
    },
    {
      title: "Total Revenue",
      value: `$${analytics.total_revenue.toLocaleString()}`,
      change: "+23.1%",
      positive: true,
      icon: Activity,
      color: "from-purple-500 to-pink-500",
    },
  ];

  return (
    <div className="min-h-screen bg-slate-950">
      {/* Sidebar + Topbar simplified */}
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
              <BarChart3 className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="font-bold text-lg text-white">SaaS Analytics</h1>
              <p className="text-xs text-slate-400">Subscription Dashboard</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-sm text-slate-400">Rajiv Kapur</span>
            <div className="w-9 h-9 rounded-full bg-indigo-600 flex items-center justify-center text-sm font-medium">
              RK
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Page title */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-white">Overview</h2>
          <p className="text-slate-400 mt-1">Track your SaaS metrics in real-time</p>
        </div>

        {/* Metric Cards */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-10">
          {cards.map((card) => (
            <div
              key={card.title}
              className="bg-slate-900 border border-slate-800 rounded-2xl p-5 hover:border-slate-700 transition"
            >
              <div className="flex items-start justify-between mb-4">
                <div
                  className={`w-11 h-11 rounded-xl bg-gradient-to-br ${card.color} flex items-center justify-center`}
                >
                  <card.icon className="w-5 h-5 text-white" />
                </div>
                <div
                  className={`flex items-center gap-1 text-xs font-medium ${
                    card.positive ? "text-emerald-400" : "text-red-400"
                  }`}
                >
                  {card.positive ? (
                    <ArrowUpRight className="w-3.5 h-3.5" />
                  ) : (
                    <ArrowDownRight className="w-3.5 h-3.5" />
                  )}
                  {card.change}
                </div>
              </div>
              <p className="text-slate-400 text-sm mb-1">{card.title}</p>
              <p className="text-2xl font-bold text-white">{card.value}</p>
            </div>
          ))}
        </div>

        {/* Bottom section */}
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Recent Activity */}
          <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6">
            <h3 className="font-semibold text-white mb-4">Recent Subscriptions</h3>
            <div className="space-y-3">
              {[
                { name: "Acme Corp", plan: "Enterprise", amount: "$299", status: "active" },
                { name: "TechStart", plan: "Pro", amount: "$79", status: "active" },
                { name: "Designify", plan: "Starter", amount: "$29", status: "active" },
                { name: "CloudBase", plan: "Pro", amount: "$79", status: "cancelled" },
                { name: "PixelForge", plan: "Enterprise", amount: "$299", status: "active" },
              ].map((item, i) => (
                <div
                  key={i}
                  className="flex items-center justify-between py-3 border-b border-slate-800 last:border-0"
                >
                  <div>
                    <p className="font-medium text-white">{item.name}</p>
                    <p className="text-xs text-slate-400">{item.plan} plan</p>
                  </div>
                  <div className="text-right">
                    <p className="font-medium text-white">{item.amount}/mo</p>
                    <span
                      className={`text-xs px-2 py-0.5 rounded-full ${
                        item.status === "active"
                          ? "bg-emerald-500/20 text-emerald-400"
                          : "bg-red-500/20 text-red-400"
                      }`}
                    >
                      {item.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Quick Stats */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
            <h3 className="font-semibold text-white mb-4">Quick Stats</h3>
            <div className="space-y-5">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-400">Active</span>
                  <span className="text-white font-medium">{analytics.active_subscribers}</span>
                </div>
                <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-500 rounded-full" style={{ width: "84%" }} />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-400">Churned this month</span>
                  <span className="text-white font-medium">{analytics.churned_this_month}</span>
                </div>
                <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                  <div className="h-full bg-orange-500 rounded-full" style={{ width: "12%" }} />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-400">Total Subscriptions</span>
                  <span className="text-white font-medium">{analytics.total_subscriptions}</span>
                </div>
                <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                  <div className="h-full bg-indigo-500 rounded-full" style={{ width: "100%" }} />
                </div>
              </div>
            </div>

            <div className="mt-8 p-4 bg-indigo-500/10 border border-indigo-500/20 rounded-xl">
              <p className="text-sm text-indigo-300">
                Connect your Stripe account to get live data via webhooks.
              </p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-sm text-slate-500">
          Built by <span className="text-slate-300">Rajiv Kapur</span> · Software Architect &
          Full Stack Developer
        </footer>
      </main>
    </div>
  );
}
