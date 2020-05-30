import React from "react";

const withPooling = (WrappedComponent) => {
  class HOC extends React.Component {
    tick() {
      this.child?.tick?.();
    }

    render() {
      return (
        <WrappedComponent
          ref={(r) => (this.child = r)}
          startPooling={() => {
            for (let i = 0; i < 100; i++)
              setTimeout(() => {
                this.tick();
              }, i * 1000);
          }}
        />
      );
    }
  }

  return HOC;
};

export default withPooling;
