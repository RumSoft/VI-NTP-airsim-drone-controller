import React from "react";

const withPooling = (WrappedComponent) => {
  class HOC extends React.Component {
    tick_id = null;
    tick() {
      this.tick_id = setTimeout(() => {
        this.child?.tick?.();
        this.tick();
      }, 300);
    }

    render() {
      return (
        <WrappedComponent
          ref={(r) => (this.child = r)}
          startPooling={() => {
            this.tick();
          }}
        />
      );
    }
  }

  return HOC;
};

export default withPooling;
