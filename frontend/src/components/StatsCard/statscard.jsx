const StatsCard = ({ title, value, change, icon }) => {
    return (
      <div className="bg-[#0B1228] border border-slate-800 rounded-2xl p-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-slate-400 text-sm">
              {title}
            </p>
  
            <h2 className="text-3xl font-bold mt-2">
              {value}
            </h2>
  
            <p className="text-green-400 text-sm mt-2">
              {change}
            </p>
          </div>
  
          <div className="text-4xl text-purple-400">
            {icon}
          </div>
        </div>
      </div>
    );
  };
  
  export default StatsCard;